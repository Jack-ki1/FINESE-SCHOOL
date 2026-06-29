"""
Chatbot Routes - Chat UI, conversation management, streaming.

SSE contract (consumed by templates/chatbot.html):
- data: {"type":"token","content":"..."}
- data: {"type":"complete","content":"..."}
- data: {"type":"error","content":"..."}
- data: [DONE]
"""

from flask import Blueprint, render_template, request, jsonify, session, Response
import uuid
import json
import logging

logger = logging.getLogger(__name__)

chatbot_bp = Blueprint('chatbot', __name__)


def _get_chat_store():
    """Get or create chat store for current session."""
    from core.chat_store import ChatStore

    sid = session.get('session_id')
    if not sid:
        sid = str(uuid.uuid4())
        session['session_id'] = sid
        session.permanent = True
    return ChatStore(sid)


@chatbot_bp.route('/')
def chat_ui():
    """Main chat UI page."""
    return render_template('chatbot.html')


@chatbot_bp.route('/api/conversations', methods=['GET'])
def list_conversations():
    """List all conversations for the session."""
    store = _get_chat_store()
    convs = store.get_all_conversations()
    return jsonify({'conversations': convs})


@chatbot_bp.route('/api/conversations', methods=['POST'])
def create_conversation():
    """Create a new conversation."""
    data = request.get_json() or {}
    title = data.get('title', 'New Chat')

    store = _get_chat_store()
    conv_id = store.create_conversation(title=title)
    conv = store.get_conversation(conv_id)
    return jsonify({'conversation': conv})


@chatbot_bp.route('/api/conversations/<conv_id>', methods=['DELETE'])
def delete_conversation(conv_id):
    """Delete a conversation."""
    store = _get_chat_store()
    if store.delete_conversation(conv_id):
        return jsonify({'success': True})
    return jsonify({'error': 'Conversation not found'}), 404


@chatbot_bp.route('/api/conversations/<conv_id>', methods=['PUT'])
def update_conversation(conv_id):
    """Update conversation title."""
    data = request.get_json() or {}
    title = data.get('title')

    if not title:
        return jsonify({'error': 'title is required'}), 400

    store = _get_chat_store()
    conv = store.get_conversation(conv_id)
    if not conv:
        return jsonify({'error': 'Conversation not found'}), 404

    success = store.rename_conversation(conv_id, title)
    if success:
        conv = store.get_conversation(conv_id)
        return jsonify({'conversation': conv})

    return jsonify({'error': 'Failed to update conversation'}), 500


@chatbot_bp.route('/api/conversations/<conv_id>/messages', methods=['GET'])
def get_messages(conv_id):
    """Get messages for a conversation."""
    store = _get_chat_store()
    conv = store.get_conversation(conv_id)
    if not conv:
        return jsonify({'error': 'Conversation not found'}), 404

    messages = store.get_messages(conv_id)
    return jsonify({'messages': messages})


@chatbot_bp.route('/api/conversations/<conv_id>/messages', methods=['POST'])
def send_message(conv_id):
    """Send a message to the conversation with streaming response (SSE)."""

    data = request.get_json() or {}
    content = (data.get('content') or '').strip()

    # Compatibility fields; currently not used by backend logic.
    _use_socratic = bool(data.get('use_socratic', False))
    _subject_area = data.get('subject_area', 'general')

    if not content:
        return jsonify({'error': 'content is required'}), 400

    store = _get_chat_store()
    conv = store.get_conversation(conv_id)
    if not conv:
        return jsonify({'error': 'Conversation not found'}), 404

    # Persist user message immediately
    store.add_message(conv_id, 'user', content)

    settings = store.get_settings()

    # Prepare messages for the LLM (history + system + current user)
    messages = store.get_messages(conv_id)
    llm_messages = [{'role': msg['role'], 'content': msg['content']} for msg in messages]

    # Prepend system message if available
    system_msg = settings.get('system_message')
    if system_msg:
        llm_messages.insert(0, {'role': 'system', 'content': system_msg})

    from services.llm_service import LLMService

    try:
        provider = LLMService.get_provider(
            settings.get('provider', 'openai'),
            model=settings.get('model'),
        )

        def generate():
            try:
                response = provider.chat(
                    messages=llm_messages,
                    temperature=settings.get('temperature', 0.7),
                    max_tokens=settings.get('max_tokens', 1024),
                )

                full = response.content or ''

                # Simulated streaming: chunk by characters.
                # (Backend providers are currently non-streaming.)
                chunk_size = 10
                for i in range(0, len(full), chunk_size):
                    chunk = full[i : i + chunk_size]
                    yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"

                yield f"data: {json.dumps({'type': 'complete', 'content': full})}\n\n"
                yield "data: [DONE]\n\n"

                # Persist assistant message after streaming completes
                store.add_message(conv_id, 'assistant', full)

            except Exception as e:
                logger.exception('Streaming error')
                yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
                yield "data: [DONE]\n\n"

        return Response(
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Access-Control-Allow-Origin': '*',
            },
        )

    except Exception as e:
        logger.exception('LLM error')
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/api/settings', methods=['GET'])
def get_settings():
    """Get current settings."""
    store = _get_chat_store()
    settings = store.get_settings()
    return jsonify(settings)


@chatbot_bp.route('/api/settings', methods=['POST'])
def update_settings():
    """Update settings."""
    data = request.get_json() or {}
    store = _get_chat_store()
    settings = store.update_settings(**data)
    return jsonify(settings)


@chatbot_bp.route('/api/providers', methods=['GET'])
def get_providers():
    """Get available LLM providers."""
    from services.llm_service import LLMService

    available = LLMService.available_providers()

    default_models = {
        'openai': 'gpt-4o-mini',
        'anthropic': 'claude-3-haiku-20240307',
        'google': 'gemini-1.5-flash',
        'huggingface': 'mistralai/Mistral-7B-Instruct-v0.3',
        'ollama': 'llama3.2',
    }

    return jsonify(
        {
            'providers': list(available.keys()),
            'configured': available,
            'default_models': default_models,
        }
    )

