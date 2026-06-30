# 🎓 FINESE SCHOOL - Modern AI Tutor Platform (Flask Version)

A powerful, modern educational AI tutor platform built with Flask, featuring glassmorphism UI, multi-model support, and streaming responses. Perfect for learning data science concepts!

## ✨ Features

### Core Features
- 🤖 **Multi-Model Support**: Switch between Hugging Face, OpenAI, Google Gemini, Anthropic models
- ⚡ **Streaming Responses**: Real-time typing effect using Server-Sent Events (SSE)
- 🎨 **Modern Glassmorphism UI**: Beautiful translucent design with animated gradients
- 🌓 **Dark/Light Theme**: Toggle between themes with persistent preferences
- 📱 **Fully Responsive**: Works perfectly on desktop, tablet, and mobile
- 📥 **PDF Export**: Download entire chat sessions for offline study
- 🎯 **Topic-Locked Conversations**: Stay focused on selected data science topics

### Educational Features
- 🧠 **Socratic Method**: Guided questioning to promote critical thinking
- 💻 **Code Examples**: Runnable code snippets with syntax highlighting
- 💡 **Best Practices**: Expert tips and common pitfalls
- 🔍 **Diagnosis**: AI identifies potential misunderstandings
- 📊 **Session Statistics**: Track questions asked and topics covered

### Technical Excellence
- 🚀 **Pure Tech Stack**: Python + HTML/CSS/JavaScript only (no frameworks!)
- 🔒 **Secure**: API keys never exposed to frontend
- ⚙️ **Configurable**: Easy environment variable configuration
- 📦 **Lightweight**: Minimal dependencies, fast performance

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- A Hugging Face API token (free at https://huggingface.co/settings/tokens)

### Installation

1. **Clone or navigate to the project:**
```bash
cd FINESE-SCHOOL
```

2. **Install dependencies:**
```bash
pip install -r requirements_flask.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
```

4. **Edit `.env` file and add your API key:**
```env
HUGGINGFACE_API_KEY=your_actual_token_here
API_TYPE=huggingface
MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
```

5. **Run the application:**
```bash
py app.py
```

6. **Open your browser:**
Visit http://localhost:5000

## 🎯 Usage Guide

### Selecting a Topic
1. Choose from available topics in the sidebar:
   - Python Programming
   - Data Analysis with Pandas & NumPy
   - SQL
   - Machine Learning
   - Deep Learning
   - Data Visualization
   - Power BI

### Asking Questions
1. Type your question in the input area
2. Press Enter or click "Get Expert Answer"
3. Watch the streaming response appear in real-time
4. Review diagnosis, code examples, and best practices

### Managing Conversations
- **Clear Chat**: Click the trash icon in sidebar
- **Export PDF**: Click export button to download session
- **Toggle Theme**: Click theme button to switch dark/light mode

## 🏗️ Project Structure

```
FINESE-SCHOOL/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── chat_engine.py             # Core chat logic
├── models.py                  # Pydantic data models
├── pdf_export.py              # PDF generation
├── utils.py                   # Utility functions
├── requirements_flask.txt     # Dependencies
├── .env.example               # Environment template
├── static/
│   └── css/
│       └── style.css          # Glassmorphism styles
├── templates/
│   └── index.html             # Main interface (inline JS)
└── src/                       # Existing modules (reused)
    ├── __init__.py
    ├── chat_engine.py
    ├── config.py
    ├── models.py
    ├── pdf_export.py
    └── utils.py
```

## 🎨 Design System

### Glassmorphism Components
- Semi-transparent backgrounds with blur effects
- Subtle borders and shadows for depth
- Smooth hover animations
- Gradient overlays

### Color Palette
**Light Theme:**
- Primary: Blue (#4285f4)
- Secondary: Red (#ea4335)
- Accent: Green (#34a853)

**Dark Theme:**
- Primary: Light Blue (#8ab4f8)
- Secondary: Light Red (#f28b82)
- Accent: Light Green (#81c995)

### Animations
- Animated gradient background (15s loop)
- Fade-in message transitions
- Hover scale effects
- Typing indicator bounce

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_DEBUG` | Enable debug mode | `true` |
| `SECRET_KEY` | Flask secret key | `dev-key` |
| `PORT` | Server port | `5000` |
| `API_TYPE` | LLM provider | `huggingface` |
| `HUGGINGFACE_API_KEY` | HF API token | Required |
| `MODEL_NAME` | Model identifier | `mistralai/Mistral-7B-Instruct-v0.2` |
| `TEMPERATURE` | Response randomness | `0.3` |
| `MAX_TOKENS` | Max response length | `2048` |

### Supported Models

**Hugging Face:**
- mistralai/Mistral-7B-Instruct-v0.2
- meta-llama/Llama-3-8b-chat-hf
- google/flan-t5-xxl
- HuggingFaceH4/zephyr-7b-beta

**Google Gemini:**
- gemini-1.5-flash
- gemini-1.5-pro
- gemini-1.5-ultra

**OpenAI:**
- gpt-4o
- gpt-4-turbo
- gpt-3.5-turbo

**Anthropic:**
- claude-3-5-sonnet-20240620
- claude-3-opus-20240229
- claude-3-haiku-20240307

## 🌐 API Endpoints

### POST /api/chat
Standard chat endpoint (non-streaming)

**Request:**
```json
{
  "topic": "Python",
  "question": "What is a list comprehension?"
}
```

**Response:**
```json
{
  "is_on_topic": true,
  "diagnosis": "User wants to understand Python list comprehensions",
  "answer": "List comprehensions provide...",
  "code_example": "[x**2 for x in range(10)]",
  "best_practice_tip": "Use for simple transformations",
  "references": ["https://docs.python.org/3/tutorial/datastructures.html"]
}
```

### POST /api/chat/stream
Streaming chat endpoint using SSE

**Request:** Same as above

**Response:** Server-Sent Events stream
```
data: {"type": "diagnosis", "content": "..."}
data: {"type": "answer_chunk", "content": "..."}
data: {"type": "code", "content": "..."}
data: {"type": "tip", "content": "..."}
data: {"type": "complete"}
```

### POST /api/export-pdf
Export chat history to PDF

**Request:**
```json
{
  "history": [
    {"sender": "user", "content": "Question"},
    {"sender": "bot", "content": "Answer"}
  ]
}
```

**Response:** PDF file download

### GET /api/topics
Get all available topics

**Response:**
```json
{
  "Python": {
    "name": "Python",
    "description": "...",
    "domain": "programming"
  }
}
```

## 🎓 Educational Approach

### Socratic Method
The AI tutor uses guided questioning to help you discover answers:
1. Clarification questions
2. Assumption exploration
3. Knowledge application

### Structured Responses
Every answer includes:
- **Diagnosis**: What you might be misunderstanding
- **Explanation**: Clear, step-by-step breakdown
- **Code Example**: Minimal, runnable code
- **Best Practice**: Key tip or warning
- **References**: Official documentation links

### Topic Enforcement
Questions are validated against selected topic to maintain focus and prevent confusion.

## 🔒 Security

### Best Practices Implemented
- ✅ API keys stored in environment variables only
- ✅ No sensitive data exposed in frontend
- ✅ Input sanitization with bleach library
- ✅ Rate limiting (configurable)
- ✅ Session management

### Production Recommendations
1. Change `SECRET_KEY` to a strong random value
2. Set `FLASK_DEBUG=false`
3. Use Redis for session storage
4. Enable HTTPS
5. Add authentication if needed
6. Configure CORS properly

## 🚀 Deployment

### Local Development
```bash
py app.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements_flask.txt .
RUN pip install --no-cache-dir -r requirements_flask.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t finese-school .
docker run -p 5000:5000 --env-file .env finese-school
```

## 🧪 Testing

Run tests (if test suite exists):
```bash
py -m pytest tests/
```

## 📊 Performance Tips

### Optimization Strategies
1. **Caching**: Implement LRU cache for frequent questions
2. **Lazy Loading**: Load heavy resources on demand
3. **Debouncing**: Delay rapid user inputs
4. **Compression**: Enable gzip for responses
5. **CDN**: Use CDN for fonts and static assets

### Monitoring
- Check Flask logs for errors
- Monitor API rate limits
- Track response times
- Watch memory usage

## 🐛 Troubleshooting

### Common Issues

**Problem**: Module not found error  
**Solution**: Ensure all dependencies installed: `pip install -r requirements_flask.txt`

**Problem**: API key error  
**Solution**: Verify `.env` file exists and contains valid API key

**Problem**: Port already in use  
**Solution**: Change PORT in `.env` or kill existing process

**Problem**: CSS not loading  
**Solution**: Check `static/css/style.css` exists and path is correct

**Problem**: Streaming not working  
**Solution**: Ensure browser supports EventSource API (all modern browsers do)

### Getting Help
1. Check this README
2. Review error messages in browser console
3. Check Flask terminal output
4. Verify environment variables
5. Test with different model

## 🌟 What Makes This Special

### For Students
- **No JavaScript Frameworks**: Demonstrates mastery of fundamentals
- **Modern Design**: Professional presentation quality
- **Educational Focus**: Built for learning, not just chatting
- **Free to Use**: Open source with free tier models

### For Developers
- **Clean Architecture**: Well-organized, modular code
- **Easy to Extend**: Add new features quickly
- **Production Ready**: Includes security and deployment configs
- **Documentation**: Comprehensive guides and examples

## 🔮 Future Enhancements

Planned features:
- [ ] Voice input/output
- [ ] Collaborative study sessions
- [ ] Advanced analytics dashboard
- [ ] Mobile app version
- [ ] Jupyter Notebook integration
- [ ] GitHub Classroom sync
- [ ] Quiz generation
- [ ] Progress badges and gamification

## 📚 Resources

### Research Sources
- [SocraticLM](https://github.com/Ljyustc/SocraticLM)
- [DeepTutor](https://github.com/HKUDS/DeepTutor)
- [Hugging Face Models](https://huggingface.co/models)
- [Glassmorphism Design](https://ui.glass)

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [CSS Backdrop Filter](https://developer.mozilla.org/en-US/docs/Web/CSS/backdrop-filter)

## 📝 License

MIT License - Feel free to use for educational purposes!

## 👨‍💻 Author

Built by a senior data science student for classroom presentation.

## 🙏 Acknowledgments

- Hugging Face for open-source models
- Flask community for excellent framework
- Google Fonts for beautiful typography
- All open-source contributors

---

**Enjoy learning with FINESE SCHOOL! 🚀**

*Last Updated: 2026-06-30*  
*Version: 2.0 (Flask Transformation)*
