"""
Chatbot Routes - Chat UI, conversation management, streaming.
"""
from flask import Blueprint, render_template, request, jsonify, session, Response, stream_with_context
import uuid
import json

chatbot_bp = Blueprint('chatbot', __name__)


def get_chat_store():
    """Get or create chat store for current session."""
    from core.chat_store import ChatStore
    sid = session.get('session_id')
    if not sid:
        sid = str(uuid.uuid4())
        session['session_id'] = sid
        session.permanent = True
    return ChatStore(sid)


@chatbot_bp.route('/chat')
def chat():
    """Main chat interface."""
    store = get_chat_store()
    conversations = store.get_all_conversations()
    active_conv = store.get_active_conversation()
    
    # Create default conversation if none exists
    if not active_conv:
        conv_id = store.create_conversation("New Chat")
        active_conv = store.get_conversation(conv_id)
        conversations = store.get_all_conversations()
    
    return render_template(
        'chatbot.html',
        conversations=conversations,
        active_conversation=active_conv,
        settings=store.get_settings(),
    )


@chatbot_bp.route('/api/conversations', methods=['GET'])
def list_conversations():
    """List all conversations."""
    store = get_chat_store()
    return jsonify({'conversations': store.get_all_conversations()})


@chatbot_bp.route('/api/conversations', methods=['POST'])
def create_conversation():
    """Create a new conversation."""
    store = get_chat_store()
    data = request.get_json() or {}
    title = data.get('title', 'New Chat')
    conv_id = store.create_conversation(title)
    return jsonify({
        'success': True,
        'conversation': store.get_conversation(conv_id),
    })


@chatbot_bp.route('/api/conversations/<conv_id>', methods=['DELETE'])
def delete_conversation(conv_id):
    """Delete a conversation."""
    store = get_chat_store()
    success = store.delete_conversation(conv_id)
    return jsonify({'success': success})


@chatbot_bp.route('/api/conversations/<conv_id>/rename', methods=['POST'])
def rename_conversation(conv_id):
    """Rename a conversation."""
    store = get_chat_store()
    data = request.get_json() or {}
    success = store.rename_conversation(conv_id, data.get('title', 'Untitled'))
    return jsonify({'success': success})


@chatbot_bp.route('/api/conversations/<conv_id>/activate', methods=['POST'])
def activate_conversation(conv_id):
    """Set active conversation."""
    store = get_chat_store()
    success = store.set_active_conversation(conv_id)
    conv = store.get_conversation(conv_id)
    return jsonify({
        'success': success,
        'conversation': conv,
    })


@chatbot_bp.route('/api/conversations/<conv_id>/messages', methods=['GET'])
def get_messages(conv_id):
    """Get messages for a conversation."""
    store = get_chat_store()
    messages = store.get_messages(conv_id)
    return jsonify({'messages': messages})


@chatbot_bp.route('/api/conversations/<conv_id>/clear', methods=['POST'])
def clear_conversation(conv_id):
    """Clear all messages in a conversation."""
    store = get_chat_store()
    success = store.clear_messages(conv_id)
    return jsonify({'success': success})


@chatbot_bp.route('/api/chat', methods=['POST'])
def send_message():
    """Send a message and get a non-streaming response."""
    store = get_chat_store()
    data = request.get_json() or {}
    
    conv_id = data.get('conversation_id') or store.get_active_conversation_id()
    user_message = data.get('message', '').strip()
    
    if not conv_id or not user_message:
        return jsonify({'error': 'Missing conversation_id or message'}), 400
    
    # Add user message
    store.add_message(conv_id, 'user', user_message)
    
    # Get settings
    settings = store.get_settings()
    provider_name = data.get('provider') or settings.get('provider', 'openai')
    model = data.get('model') or settings.get('model')
    temperature = float(data.get('temperature', settings.get('temperature', 0.7)))
    max_tokens = int(data.get('max_tokens', settings.get('max_tokens', 1024)))
    system_message = data.get('system_message', settings.get('system_message', ''))
    
    # Build message history for LLM
    messages = []
    if system_message:
        messages.append({'role': 'system', 'content': system_message})
    
    # Add conversation history (last 20 messages to stay within context limits)
    conv_messages = store.get_messages(conv_id)
    for msg in conv_messages[-21:-1]:  # Exclude the just-added user message
        messages.append({'role': msg['role'], 'content': msg['content']})
    messages.append({'role': 'user', 'content': user_message})
    
    try:
        from services.llm_service import LLMService
        provider = LLMService.get_provider(provider_name, model=model)
        
        # Anthropic uses 'system' param separately
        kwargs = {'temperature': temperature, 'max_tokens': max_tokens}
        if provider_name == 'anthropic' and system_message:
            kwargs['system'] = system_message
            messages = [m for m in messages if m['role'] != 'system']
        
        response = provider.chat(messages, **kwargs)
        
        # Add assistant message
        store.add_message(conv_id, 'assistant', response.content, metadata={
            'model': response.model,
            'provider': response.provider,
            'usage': response.usage,
        })
        
        return jsonify({
            'success': True,
            'response': response.content,
            'model': response.model,
            'provider': response.provider,
            'usage': response.usage,
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/api/chat/stream', methods=['POST'])
def send_message_stream():
    """Send a message and stream the response."""
    store = get_chat_store()
    data = request.get_json() or {}
    
    conv_id = data.get('conversation_id') or store.get_active_conversation_id()
    user_message = data.get('message', '').strip()
    
    if not conv_id or not user_message:
        return jsonify({'error': 'Missing conversation_id or message'}), 400
    
    # Add user message
    store.add_message(conv_id, 'user', user_message)
    
    # Get settings
    settings = store.get_settings()
    provider_name = data.get('provider') or settings.get('provider', 'openai')
    model = data.get('model') or settings.get('model')
    temperature = float(data.get('temperature', settings.get('temperature', 0.7)))
    max_tokens = int(data.get('max_tokens', settings.get('max_tokens', 1024)))
    system_message = data.get('system_message', settings.get('system_message', ''))
    
    # Build message history
    messages = []
    if system_message:
        messages.append({'role': 'system', 'content': system_message})
    
    conv_messages = store.get_messages(conv_id)
    for msg in conv_messages[-21:-1]:
        messages.append({'role': msg['role'], 'content': msg['content']})
    messages.append({'role': 'user', 'content': user_message})
    
    def generate():
        from services.llm_service import LLMService
        provider = LLMService.get_provider(provider_name, model=model)
        
        kwargs = {'temperature': temperature, 'max_tokens': max_tokens}
        if provider_name == 'anthropic' and system_message:
            kwargs['system'] = system_message
            messages_stream = [m for m in messages if m['role'] != 'system']
        else:
            messages_stream = messages
        
        full_response = []
        try:
            for chunk in provider.chat_stream(messages_stream, **kwargs):
                full_response.append(chunk)
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            
            # Save complete response
            complete_text = ''.join(full_response)
            store.add_message(conv_id, 'assistant', complete_text, metadata={
                'model': model or provider.model,
                'provider': provider_name,
            })
            
            yield f"data: {json.dumps({'done': True, 'full_response': complete_text})}\n\n"
        
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
        }
    )


@chatbot_bp.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify(_get_settings())


@chatbot_bp.route('/api/settings', methods=['POST'])
def update_settings():
    data = request.get_json() or {}
    settings = _get_settings()
    for key in ['provider', 'model', 'temperature', 'max_tokens', 'system_message']:
        if key in data:
            settings[key] = data[key]
    session['settings'] = settings
    return jsonify(settings)


@chatbot_bp.route('/api/providers', methods=['GET'])
def get_providers():
    from services.llm_service import LLMService
    return jsonify({
        'providers': list(LLMService.PROVIDERS.keys()),
        'default_models': LLMService.DEFAULT_MODELS,
        'configured': {p: bool(LLMService.PROVIDERS[p].get('key')) for p in LLMService.PROVIDERS},
    })