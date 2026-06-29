# ChatBot Pro - Flask Edition

A production-ready, multi-provider AI chatbot built with **Flask**, inspired by the architecture of [FINESE_2](https://github.com/Jack-ki1/FINESE_2/). This is a complete rebuild of the original Hugging Face Space `chatbot1` as a modular, extensible Flask application.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Quick Start](#quick-start)
4. [Supported LLM Providers](#supported-llm-providers)
5. [Key Features](#key-features)
6. [API Endpoints](#api-endpoints)
7. [Configuration](#configuration)
8. [Extending the Chatbot](#extending-the-chatbot)
9. [Troubleshooting](#troubleshooting)
10. [License](#license)

---

## Architecture Overview

| Layer | Files | Purpose |
|-------|-------|---------|
| **Entry Point** | `app.py` | Flask app factory, blueprint registration, session config |
| **Config** | `config.py` | Global constants, API keys, defaults |
| **Core** | `core/chat_store.py`, `core/document_store.py` | Server-side pickle persistence for chats & documents |
| **Services** | `services/llm_service.py` | Multi-provider LLM abstraction (OpenAI, Anthropic, Google, HF, Ollama) |
| **Routes** | `routes/main.py`, `routes/chatbot.py`, `routes/api.py` | Flask blueprints for UI, chat API, and file upload |
| **Templates** | `templates/*.html` | Jinja2 + Bootstrap 5 frontend |
| **Static** | `static/css/style.css`, `static/js/main.js` | Custom styles and shared JS utilities |

---

## Project Structure

```
chatbot_flask/
├── app.py                          # Flask entry point
├── config.py                       # Global configuration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
│
├── core/                           # Data persistence layer
│   ├── __init__.py
│   ├── chat_store.py              # Conversation & message storage (pickle)
│   └── document_store.py          # Uploaded file storage for RAG
│
├── services/                       # Business logic
│   ├── __init__.py
│   └── llm_service.py             # Multi-provider LLM integration
│
├── routes/                         # Flask blueprints
│   ├── __init__.py                # Blueprint exports
│   ├── main.py                    # Home & settings pages
│   ├── chatbot.py                 # Chat API, streaming, conversations
│   └── api.py                     # File upload & document management
│
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                  # Master layout (Bootstrap 5)
│   ├── chatbot.html               # Main chat interface
│   └── settings.html              # Configuration & provider status
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css              # Custom styles
│   ├── js/
│   │   └── main.js                # Shared JS utilities
│   └── uploads/                   # Temporary file storage
│       └── .gitkeep
│
└── flask_session/                  # Server-side session files (auto-created)
    ├── chats/                      # Pickled conversation data
    └── docs/                       # Pickled document data
```

---

## Quick Start

### Prerequisites

- **Python**: 3.10 or higher
- **pip**: Latest version
- **Memory**: 2GB RAM minimum (4GB+ recommended for local models)

### 1. Clone & Setup

```bash
git clone <your-repo-url> chatbot_flask
cd chatbot_flask

python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Run

```bash
# Development
py app.py

# Production (Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Open **http://127.0.0.1:5000** — the app will automatically create a default conversation on first load.

---

## Supported LLM Providers

| Provider | Package Required | Environment Variable | Default Model |
|----------|---------------|----------------------|---------------|
| **OpenAI** | `openai` | `OPENAI_API_KEY` | `gpt-4o-mini` |
| **Anthropic** | `anthropic` | `ANTHROPIC_API_KEY` | `claude-3-haiku-20240307` |
| **Google** | `google-generativeai` | `GOOGLE_API_KEY` | `gemini-1.5-flash` |
| **Hugging Face** | `requests` (built-in) | `HF_TOKEN` | `mistralai/Mistral-7B-Instruct-v0.3` |
| **Ollama** | `requests` (built-in) | None (local) | `llama3.2` |

Install only the packages you need:
```bash
pip install openai anthropic google-generativeai
```

---

## Key Features

- **Multi-Provider LLM Support**: Switch between OpenAI, Anthropic, Google, Hugging Face, and local Ollama models
- **Streaming Responses**: Real-time token streaming via Server-Sent Events (SSE)
- **Persistent Conversations**: Multiple chat threads with server-side pickle storage
- **Document Upload**: Upload `.txt`, `.csv`, `.py`, `.md` files for RAG context
- **Session-Based Settings**: Per-user provider/model/temperature configuration
- **Responsive UI**: Bootstrap 5 with sidebar conversation list and collapsible settings panel
- **Modular Architecture**: Easy to extend with new providers or features

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/chat` | Main chat UI |
| `GET` | `/settings` | Settings page |
| `GET` | `/api/conversations` | List all conversations |
| `POST` | `/api/conversations` | Create new conversation |
| `DELETE` | `/api/conversations/<id>` | Delete conversation |
| `POST` | `/api/conversations/<id>/rename` | Rename conversation |
| `POST` | `/api/conversations/<id>/activate` | Set active conversation |
| `GET` | `/api/conversations/<id>/messages` | Get messages |
| `POST` | `/api/conversations/<id>/clear` | Clear messages |
| `POST` | `/api/chat` | Send message (non-streaming) |
| `POST` | `/api/chat/stream` | Send message (streaming SSE) |
| `GET` | `/api/settings` | Get current settings |
| `POST` | `/api/settings` | Update settings |
| `GET` | `/api/providers` | List available providers |
| `POST` | `/api/upload` | Upload file |
| `GET` | `/api/documents` | List uploaded documents |
| `DELETE` | `/api/documents/<id>` | Delete document |

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=development

# LLM Provider API Keys (add only the ones you plan to use)
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GOOGLE_API_KEY=your-google-generative-ai-key-here
HF_TOKEN=hf_your-huggingface-token-here

# Optional: Ollama base URL (default: http://localhost:11434)
# OLLAMA_BASE_URL=http://localhost:11434
```

### Per-Session Settings

Users can change provider, model, temperature, max tokens, and system message via the settings panel in the chat UI. These are stored per-session in `ChatStore`.

---

## Extending the Chatbot

### Adding a New LLM Provider

1. Create a new class in `services/llm_service.py` inheriting from `BaseLLMProvider`
2. Implement `chat()` and optionally `chat_stream()` methods
3. Register it in `LLMService.PROVIDERS` and `LLMService.DEFAULT_MODELS`
4. Add the provider option to the settings dropdown in `templates/chatbot.html`

### Adding Vector DB for RAG

Replace `DocumentStore.get_combined_context()` with a proper vector search:
1. Chunk documents on upload
2. Store embeddings in ChromaDB / Pinecone / Weaviate
3. Retrieve relevant chunks at query time

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `KeyError: 'session_id'` | Clear browser cookies and refresh |
| Upload fails with 413 | Increase `MAX_CONTENT_LENGTH` in `config.py` |
| Session lost on refresh | Verify `flask_session/` directory exists and is writable |
| LLM returns error | Check API key in `.env` and provider status on `/settings` |
| Ollama not connecting | Ensure Ollama is running: `ollama serve` |

---

## License

MIT License
```

---

## File Summary Table

| File | Lines | Purpose |
|------|-------|---------|
| `config.py` | 45 | Global constants, API keys, defaults |
| `core/__init__.py` | 1 | Package marker |
| `core/chat_store.py` | 155 | Conversation persistence with pickle |
| `core/document_store.py` | 85 | File upload persistence for RAG |
| `services/__init__.py` | 1 | Package marker |
| `services/llm_service.py` | 315 | 5 LLM providers (OpenAI, Anthropic, Google, HF, Ollama) |
| `routes/__init__.py` | 6 | Blueprint exports |
| `routes/main.py` | 22 | Home redirect + settings page |
| `routes/chatbot.py` | 215 | 13 API endpoints for chat & conversations |
| `routes/api.py` | 55 | File upload & document management |
| `static/js/main.js` | 95 | Shared JS utilities (toast, clipboard, debounce) |
| `README.md` | 280 | Full documentation |

All files are syntactically verified and ready to run.

# FINESE SCHOOL - AI Assistant for Data Professionals

<p align="center">
  <strong>Use any AI of your choice to master SQL, Python, data analysis, and visualization.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/flask-3.0-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
</p>

---

## Features

### AI Chat
- **Multi-Provider Support**: OpenAI, Anthropic, Google Gemini, HuggingFace, Ollama (local)
- **Streaming Responses**: Real-time token-by-token output
- **Markdown Rendering**: Code blocks with syntax highlighting
- **Document RAG**: Upload documents for context-aware conversations
- **Conversation Management**: Multiple conversations, rename, delete, export

### Data Workspace
- **SQL Editor**: CodeMirror-based editor with syntax highlighting
- **Database Connectivity**: SQLite, MySQL, PostgreSQL, SQL Server
- **Natural Language to SQL**: Describe what you want, AI writes the query
- **Python Code Execution**: Sandboxed execution with pandas, numpy, matplotlib
- **Data Visualization**: Auto-generate charts with Plotly.js
- **CSV/Excel Analysis**: Upload data files for AI-powered analysis

### Learning Hub
- **Structured Learning Paths**: SQL, Python, Data Visualization, Machine Learning
- **Interactive Exercises**: Practice with instant feedback
- **AI Tutor**: Ask questions and get personalized explanations
- **Progress Tracking**: Monitor your learning journey

### Production Ready
- **Docker Support**: One-command deployment
- **Rate Limiting**: Protection against API abuse
- **Structured Logging**: Debug and monitor with ease
- **Export**: Download conversations, query results, analysis

## Quick Start

### Local Development

```bash
# Clone and setup
git clone <repo-url>
cd finese-school

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run
python app.py
```

Visit `http://localhost:5000`

### Docker

```bash
cp .env.example .env
# Edit .env with your API keys

docker compose up -d
```

Visit `http://localhost:5000`

### With Local AI (Ollama)

```bash
docker compose --profile local-ai up -d
```

## Configuration

Set these in your `.env` file:

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `GOOGLE_API_KEY` | Google Gemini API key |
| `HF_TOKEN` | HuggingFace token |
| `OLLAMA_BASE_URL` | Ollama server URL (default: http://localhost:11434) |
| `FLASK_SECRET_KEY` | Flask session secret key |
| `DATABASE_URL` | Database URL (default: sqlite:///finese_school.db) |

## Project Structure

```
finese-school/
├── app.py                    # Flask application entry point
├── config.py                 # Configuration and learning paths
├── models/                   # SQLAlchemy models
│   ├── conversation.py       # Chat conversations & messages
│   ├── database_connection.py # DB connection configs
│   └── learning.py           # Learning progress & exercises
├── core/                     # Core services
│   ├── code_executor.py      # Sandboxed Python execution
│   ├── database_service.py   # SQL execution & schema introspection
│   ├── data_analyzer.py      # CSV/Excel analysis & visualization
│   └── vector_store.py       # ChromaDB RAG vector store
├── services/
│   └── llm_service.py        # Multi-provider LLM abstraction
├── routes/                   # Flask blueprints
│   ├── main.py               # Dashboard, workspace pages
│   ├── chatbot.py            # Chat UI & streaming API
│   ├── api.py                # File upload, export
│   ├── data.py               # SQL, Python, data analysis endpoints
│   └── education.py          # Learning paths, exercises, AI tutor
├── templates/                # Jinja2 HTML templates
├── static/                   # CSS, JS, uploads
├── tests/                    # Pytest test suite
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   Browser                        │
│  (CodeMirror, Plotly.js, marked.js, Prism.js)   │
└──────────────────────┬──────────────────────────┘
                       │ HTTP / SSE
┌──────────────────────┴──────────────────────────┐
│              Flask Application                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │
│  │  Routes  │ │  Models  │ │   Core Services  │ │
│  │ (API)    │ │ (SQLA)   │ │  (Executors)     │ │
│  └────┬─────┘ └────┬─────┘ └──┬───┬───┬───────┘ │
│       │            │          │   │   │         │
│  ┌────┴────────────┴──────────┴───┴───┴───────┐ │
│  │           LLM Service (Multi-Provider)      │ │
│  └──┬──────┬──────┬──────┬──────┬─────────────┘ │
└─────┼──────┼──────┼──────┼──────┼───────────────┘
      │      │      │      │      │
  OpenAI  Anthropic Google   HF   Ollama
```

## License

MIT
#   F I N E S E - S C H O O L  
 