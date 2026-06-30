import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv
import re
from src.config import TOPIC_REGISTRY
from src.chat_engine import generate_structured_response
from src.pdf_export import export_chat_to_pdf
from src.utils import detect_language_from_context, sanitize_input

# Load environment variables
if os.getenv("IS_DOCKER") != "true":
    load_dotenv()

def highlight_text(text):
    """Highlight important keywords in the text."""
    keywords = ["important", "note", "remember", "key", "tip", "⚠️", "only", "strictly", "best practice", "crucial", "essential"]
    sentences = text.split(". ")
    highlighted_sentences = []
    for sent in sentences:
        if any(kw.lower() in sent.lower() for kw in keywords):
            sent = f'<span style="background-color:#fff3cd; color:#856404; font-weight:bold;">{sent.strip()}.</span>'
        else:
            sent = sent.strip() + "." if sent.strip() else ""
        highlighted_sentences.append(sent)
    return ". ".join(filter(None, highlighted_sentences))

# Configure page
st.set_page_config(page_title="FINESE SCHOOL: Data Science Mentor", page_icon="🎓", layout="wide")

# Define provider key mapping
PROVIDER_KEY_MAPPING = {
    "Google Gemini": "google",
    "OpenAI": "openai",
    "Hugging Face": "huggingface",
    "Anthropic": "anthropic"
}

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "llm_provider" not in st.session_state:
    st.session_state.llm_provider = "Google Gemini"
if "llm_api_key" not in st.session_state:
    st.session_state.llm_api_key = ""
if "llm_model" not in st.session_state:
    st.session_state.llm_model = ""
    
if "current_topic" not in st.session_state:
    st.session_state.current_topic = list(TOPIC_REGISTRY.keys())[0] if TOPIC_REGISTRY else None

# Apply custom CSS
st.markdown("""
<style>
    .diagnosis {
        background-color: #fff8e1;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid #ffc107;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .tip {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .refs {
        background-color: #f3e5f5;
        border-left: 5px solid #9c27b0;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stButton>button {
        border-radius: 10px;
    }
    .chat-message {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 5px solid #757575;
    }
    .highlight-keyword {
        background-color: #fff3cd;
        color: #856404;
        font-weight: bold;
    }
    .topic-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #fafafa;
        transition: transform 0.2s;
    }
    .topic-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .topic-title {
        font-weight: bold;
        font-size: 1.1em;
        margin-bottom: 5px;
    }
    .topic-description {
        color: #666;
        font-size: 0.9em;
    }
    .welcome-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        text-align: center;
    }
    .stats-card {
        background-color: #e3f2fd;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }
    .code-block {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        overflow-x: auto;
        font-family: monospace;
        font-size: 0.9em;
        margin: 15px 0;
        border: 1px solid #eee;
    }
    .on-topic-warning {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="welcome-banner"><h1>🎓 FINESE SCHOOL: Your 24/7 Data Mentor</h1><p>Get expert-level, topic-locked, code-rich answers with best practices</p></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings & Controls")
    
    # Theme selector
    theme = st.selectbox("🎨 Theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown("""
        <style>
            .stApp {
                background-color: #0e1117;
                color: white;
            }
            .stMarkdown, .stText {
                color: white;
            }
            .topic-card {
                background-color: #262730;
                color: white;
            }
            .topic-description {
                color: #ccc;
            }
        </style>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("🤖 LLM Provider")
    llm_provider = st.selectbox(
        "Select LLM Provider",
        ["Google Gemini", "OpenAI", "Hugging Face", "Anthropic", "None"],
        index=0,
        key="llm_provider"
    )

    provider_key = PROVIDER_KEY_MAPPING.get(llm_provider, "")
    if llm_provider != "None" and provider_key:
        api_key = st.text_input(
            f"{llm_provider} API Key",
            type="password",
            key=f"{provider_key}_api_key",
            help="Enter your API key for the selected provider"
        )
        
    # Define provider-specific model options
    PROVIDER_MODELS = {
        "Google Gemini": [
            "gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.5-advanced",
            "gemini-1.0-pro", "gemini-1.5-ultra"
        ],
        "OpenAI": [
            "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo",
            "gpt-4", "gpt-4-32k"
        ],
        "Hugging Face": [
            "mistralai/Mistral-7B-Instruct-v0.2", "meta-llama/Llama-3-8b-chat-hf",
            "google/flan-t5-xxl", "HuggingFaceH4/zephyr-7b-beta"
        ],
        "Anthropic": [
            "claude-3-5-sonnet-20240620", "claude-3-opus-20240229",
            "claude-3-haiku-20240307", "claude-2.1"
        ]
    }
    
    # Get models for selected provider
    model_options = PROVIDER_MODELS.get(llm_provider, [])
    model_options.append("Custom Model")
    
    # Use the extracted model options in the selectbox
    model_name = st.selectbox(
        "Model Name",
        options=model_options,
        key=f"{provider_key}_model",
        help="Select a model name or choose 'Custom Model' to enter your own"
    )

    # Simplify the custom model input logic
    if model_name == "Custom Model":
        custom_model_name = st.text_input(
            "Enter a custom model name",
            placeholder="Type your model name here...",
            key=f"{provider_key}_custom_model"
        )
        if not custom_model_name.strip():
            st.error("Custom model name cannot be empty.")
    else:
        custom_model_name = None

 
    # Stats
    st.divider()
    st.subheader("📊 Session Stats")
    st.markdown(f'<div class="stats-card"><h3>{len(st.session_state.chat_history)//2}</h3><p>Questions Asked</p></div>', unsafe_allow_html=True)
    
    # Topic information
    st.divider()
    st.subheader("📘 Topics")
    for topic_key, topic_spec in TOPIC_REGISTRY.items():
        with st.expander(topic_key):
            st.markdown(f"""
            <div class="topic-card">
                <div class="topic-title">{topic_spec.name}</div>
                <div class="topic-description">{topic_spec.description}</div>
                <div style="margin-top: 10px;">
                    <strong>Domain:</strong> {topic_spec.domain}<br>
                    <strong>Allowed Libraries:</strong> {', '.join(topic_spec.allowed_libraries) or 'None'}<br>
                    <strong>Banned Topics:</strong> {', '.join(topic_spec.banned_topics) or 'None'}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Conversation history controls
    st.divider()
    st.subheader("🗂️ Conversation")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.chat_history = []
            st.success("History cleared!")
            st.rerun()
            
    with col2:
        if st.button("📥 Export to PDF", use_container_width=True):
            if st.session_state.chat_history:
                try:
                    with st.spinner("Generating PDF..."):
                        pdf_bytes = export_chat_to_pdf(st.session_state.chat_history)
                        st.download_button(
                            "✅ Download PDF", 
                            pdf_bytes, 
                            "data_mentor_session.pdf", 
                            "application/pdf",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"PDF generation failed: {str(e)}")
                    st.info("Please try again or contact support if the issue persists.")
            else:
                st.warning("No conversation to export")
    
    # Info
    st.divider()
    st.subheader("ℹ️ About")
    st.info("FINESE SCHOOL provides expert-level answers on data science topics with code examples and best practices.")

# API Key validation - MOVED AFTER SIDEBAR
current_provider = st.session_state.llm_provider
if current_provider != "None":
    provider_key = PROVIDER_KEY_MAPPING.get(current_provider, "")
    if provider_key:
        api_key = st.session_state.get(f"{provider_key}_api_key", "")
        if not api_key:
            st.error(f"⚠️ {current_provider} API key not found. Please enter your API key in the sidebar.")
            st.stop()

# Main interface
col1, col2 = st.columns([1, 2])

with col1:
    st.header("🎯 Select Topic")
    topic_keys = list(TOPIC_REGISTRY.keys())
    selected_topic = st.selectbox("Choose your domain", topic_keys, index=topic_keys.index(st.session_state.current_topic) if st.session_state.current_topic in topic_keys else 0)
    st.session_state.current_topic = selected_topic
    
    topic_spec = TOPIC_REGISTRY[selected_topic]
    st.markdown(f"""
    <div class="topic-card">
        <div class="topic-title">Current Topic: {topic_spec.name}</div>
        <div class="topic-description">{topic_spec.description}</div>
        <div style="margin-top: 10px;">
            <strong>Style Guide:</strong> {topic_spec.style_guide}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.header("❓ Ask a Question")
    user_q = st.text_area("Enter your precise question", height=120, placeholder=f"Ask anything about {selected_topic}...")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        submit = st.button("🧠 Get Expert Answer", type="primary", use_container_width=True)
    with col_btn2:
        clear = st.button("🗑️ Clear Chat", use_container_width=True)

# Process user query
if submit and user_q.strip():
    # Sanitize input
    sanitized_question = sanitize_input(user_q.strip())
    
    if len(sanitized_question) < 10:
        st.warning("Please enter a more detailed question (at least 10 characters).")
    else:
        try:
            with st.spinner("Dr. Data is analyzing your question..."):
                # Add user question to chat
                st.session_state.chat_history.append(("🧑‍🎓 You", sanitized_question))
                
                # Generate response
                response = generate_structured_response(selected_topic, sanitized_question)
                
                if not response.is_on_topic:
                    msg = f'<div class="on-topic-warning"><strong>⚠️ Off-topic Question</strong><br>{response.answer}</div>'
                    st.session_state.chat_history.append(("🤖 Dr. Data", msg))
                else:
                    # Build rich response
                    parts = []
                    if response.diagnosis:
                        parts.append(f'<div class="diagnosis"><strong>🔍 Diagnosis:</strong> {response.diagnosis}</div>')
                    parts.append(f'<div class="answer">{response.answer}</div>')
                    if response.code_example:
                        lang = detect_language_from_context(sanitized_question, selected_topic)
                        parts.append(f'<div class="code-block">{response.code_example}</div>')
                    if response.best_practice_tip:
                        parts.append(f'<div class="tip"><strong>💡 Best Practice:</strong> {response.best_practice_tip}</div>')
                    if response.references:
                        refs = "<br>".join(f"• <a href='{r}' target='_blank'>{r}</a>" for r in response.references)
                        parts.append(f'<div class="refs"><strong>📚 References:</strong><br>{refs}</div>')
                    
                    full_response = "".join(parts)
                    # Apply highlighting to the response
                    highlighted_response = highlight_text(full_response)
                    st.session_state.chat_history.append(("🤖 Dr. Data", highlighted_response))
                
                st.rerun()
        except Exception as e:
            st.error(f"❌ Tutor error: {str(e)}")
            # Add error to chat for context
            st.session_state.chat_history.append(("🤖 Dr. Data", f"❌ Sorry, I encountered an error: {str(e)}"))

# Clear chat
if clear:
    st.session_state.chat_history = []
    st.success("Chat cleared!")
    st.rerun()

# Render chat with markdown + HTML
st.divider()
st.header("💬 Conversation")

# Limit conversation history for performance
MAX_HISTORY = 50
if len(st.session_state.chat_history) > MAX_HISTORY * 2:
    st.session_state.chat_history = st.session_state.chat_history[-MAX_HISTORY * 2:]

# Display messages
if st.session_state.chat_history:
    for sender, content in st.session_state.chat_history:
        is_user = "You" in sender
        message_class = "user-message" if is_user else "assistant-message"
        
        with st.container():
            if is_user:
                st.markdown(
                    f"""
                    <div class="chat-message {message_class}">
                        <strong>{sender}</strong>
                        <div style="margin-top: 10px;">{content}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Assistant message with enhanced styling
                st.markdown(
                    f"""
                    <div class="chat-message {message_class}">
                        <strong>{sender}</strong>
                        <div style="margin-top: 10px;">{content}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
else:
    st.info("👋 Welcome! Select a topic and ask your first question to get started.")