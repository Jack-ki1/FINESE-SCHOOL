from flask import Flask, render_template, request, jsonify, Response, stream_with_context, session
import json
import os
from dotenv import load_dotenv
from src.chat_engine import generate_structured_response
from src.pdf_export import export_chat_to_pdf
from src.config import TOPIC_REGISTRY

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# Simple session storage (in production, use Redis or database)
chat_sessions = {}


@app.route('/')
def index():
    """Render main chat interface"""
    return render_template('index.html', topics=TOPIC_REGISTRY)


@app.route('/test')
def test_page():
    """Render API test page for debugging"""
    return render_template('test_api.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Standard chat endpoint (non-streaming)"""
    try:
        data = request.json
        topic = data.get('topic')
        question = data.get('question')
        
        if not topic or not question:
            return jsonify({'error': 'Missing topic or question'}), 400
        
        # Generate response using existing chat engine
        response = generate_structured_response(topic, question)
        
        # Convert Pydantic model to dict
        return jsonify(response.dict())
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Streaming chat endpoint using SSE (Server-Sent Events)"""
    try:
        data = request.json
        topic = data.get('topic')
        question = data.get('question')
        
        # Log incoming request for debugging
        print(f"\n📨 Streaming request received:")
        print(f"   Topic: {topic}")
        print(f"   Question: {question[:50]}...")
        print(f"   API_TYPE: {os.getenv('API_TYPE', 'not set')}")
        print(f"   MODEL_NAME: {os.getenv('MODEL_NAME', 'not set') if os.getenv('API_TYPE') == 'huggingface' else os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')}")
        
        if not topic or not question:
            def error_generator():
                yield f"data: {json.dumps({'type': 'error', 'content': 'Missing topic or question'})}\n\n"
            
            return Response(
                stream_with_context(error_generator()),
                mimetype='text/event-stream'
            )
        
        def generate():
            """Generator function for SSE streaming"""
            try:
                print(f"   🔄 Generating response with {os.getenv('API_TYPE', 'unknown')} API...")
                
                # Generate structured response
                response = generate_structured_response(topic, question)
                
                print(f"   ✅ Response generated successfully!")
                print(f"   - Has diagnosis: {bool(response.diagnosis)}")
                print(f"   - Answer length: {len(response.answer)} chars")
                print(f"   - Has code: {bool(response.code_example)}")
                print(f"   - Has tip: {bool(response.best_practice_tip)}")
                
                # Send diagnosis if available
                if response.diagnosis:
                    yield f"data: {json.dumps({'type': 'diagnosis', 'content': response.diagnosis})}\n\n"
                
                # Stream the answer character by character to simulate typing
                answer = response.answer
                chunk_count = 0
                for i in range(0, len(answer), 10):
                    chunk = answer[i:i+10]
                    yield f"data: {json.dumps({'type': 'answer_chunk', 'content': chunk})}\n\n"
                    chunk_count += 1
                
                print(f"   📤 Sent {chunk_count} answer chunks")
                
                # Send code example if available
                if response.code_example:
                    yield f"data: {json.dumps({'type': 'code', 'content': response.code_example})}\n\n"
                    print(f"   📝 Sent code example")
                
                # Send best practice tip if available
                if response.best_practice_tip:
                    yield f"data: {json.dumps({'type': 'tip', 'content': response.best_practice_tip})}\n\n"
                    print(f"   💡 Sent best practice tip")
                
                # Send completion signal
                yield f"data: {json.dumps({'type': 'complete'})}\n\n"
                print(f"   ✅ Streaming complete\n")
                
            except Exception as e:
                print(f"   ❌ Error during streaming: {str(e)}")
                import traceback
                traceback.print_exc()
                yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
        
        return Response(
            stream_with_context(generate()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no'  # Disable nginx buffering
            }
        )
    
    except Exception as e:
        print(f"❌ Endpoint error: {str(e)}")
        import traceback
        traceback.print_exc()
        def error_generator():
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
        
        return Response(
            stream_with_context(error_generator()),
            mimetype='text/event-stream'
        )


@app.route('/api/export-pdf', methods=['POST'])
def export_pdf():
    """Export chat history to PDF"""
    try:
        data = request.json
        chat_history = data.get('history', [])
        
        if not chat_history:
            return jsonify({'error': 'No chat history to export'}), 400
        
        pdf_bytes = export_chat_to_pdf(chat_history)
        
        return Response(
            pdf_bytes,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': 'attachment; filename=finese_school_session.pdf'
            }
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for testing"""
    return jsonify({
        'status': 'healthy',
        'message': 'FINESE SCHOOL Flask API is running',
        'version': '2.0'
    })


@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get all available topics"""
    topics_dict = {key: spec.dict() for key, spec in TOPIC_REGISTRY.items()}
    return jsonify(topics_dict)


if __name__ == '__main__':
    # Run the Flask application
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    
    print("\n" + "="*60)
    print("🎓 FINESE SCHOOL - AI Tutor Platform")
    print("="*60)
    print(f"✅ Server starting on http://localhost:{port}")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print(f"📊 Available topics: {len(TOPIC_REGISTRY)}")
    print("="*60)
    print("\nOpen your browser and visit: http://localhost:" + str(port))
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
