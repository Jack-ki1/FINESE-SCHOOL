import pdfkit
import tempfile
import os
import html
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from src.utils import strip_html
import logging

logger = logging.getLogger(__name__)

def syntax_highlight_code(code: str, language: str = "python") -> str:
    try:
        lexer = get_lexer_by_name(language)
    except:
        try:
            lexer = guess_lexer(code)
        except:
            lexer = get_lexer_by_name("text")
    formatter = HtmlFormatter(style="friendly", cssclass="codehilite")
    return highlight(code, lexer, formatter)

def render_chat_to_html(chat_history) -> str:
    css = HtmlFormatter(style="friendly").get_style_defs('.codehilite')
    html_lines = [f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'/>
        <title>FINESE SCHOOL: Data Science Mentor Session</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                padding: 30px; 
                background: #fff; 
                color: #333;
            }}
            h1 {{ 
                color: #2c3e50; 
                text-align: center;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{ 
                color: #3498db; 
                border-left: 4px solid #3498db;
                padding-left: 10px;
            }}
            .message {{ 
                margin-bottom: 25px; 
                padding: 20px; 
                border-radius: 12px; 
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .user {{ 
                background: #e3f2fd; 
                border-left: 5px solid #2196f3; 
            }}
            .assistant {{ 
                background: #f5f5f5; 
                border-left: 5px solid #757575; 
            }}
            .diagnosis {{ 
                background: #fff8e1; 
                padding: 15px; 
                border-radius: 10px; 
                margin: 15px 0; 
                border-left: 5px solid #ffc107;
            }}
            .tip {{ 
                background: #e8f5e9; 
                border-left: 5px solid #4caf50; 
                padding: 15px; 
                border-radius: 10px; 
                margin: 15px 0; 
            }}
            .refs {{ 
                background: #f3e5f5; 
                border-left: 5px solid #9c27b0; 
                padding: 15px; 
                border-radius: 10px; 
                margin: 15px 0; 
            }}
            .on-topic-warning {{
                background: #ffebee;
                border-left: 5px solid #f44336;
                padding: 15px;
                border-radius: 10px;
                margin: 15px 0;
            }}
            .code-block {{
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
                overflow-x: auto;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
                margin: 15px 0;
                border: 1px solid #eee;
            }}
            {css}
            a {{
                color: #3498db;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h1>FINESE SCHOOL: Expert Data Science Session</h1>
        <p><em>Session exported on {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
        <hr>
    """]
    
    for role, content in chat_history:
        cls = "user" if "You" in role else "assistant"
        clean_content = strip_html(content)
        
        # Handle special content blocks
        import re
        
        # Process diagnosis blocks
        clean_content = re.sub(r'<div class="diagnosis">(.*?)</div>', r'<div class="diagnosis">\1</div>', clean_content, flags=re.DOTALL)
        
        # Process tip blocks
        clean_content = re.sub(r'<div class="tip">(.*?)</div>', r'<div class="tip">\1</div>', clean_content, flags=re.DOTALL)
        
        # Process reference blocks
        clean_content = re.sub(r'<div class="refs">(.*?)</div>', r'<div class="refs">\1</div>', clean_content, flags=re.DOTALL)
        
        # Process code blocks
        def replace_code_block(match):
            code = match.group(1)
            return f'<div class="code-block"><pre>{html.escape(code)}</pre></div>'
        
        clean_content = re.sub(r'<div class="codehilite">(.*?)</div>', replace_code_block, clean_content, flags=re.DOTALL)
        
        # Process on-topic warnings
        clean_content = re.sub(r'<div class="on-topic-warning">(.*?)</div>', r'<div class="on-topic-warning">\1</div>', clean_content, flags=re.DOTALL)
        
        html_lines.append(f'<div class="message {cls}"><h2>{role}</h2><div>{clean_content}</div></div>')
    
    html_lines.append("</body></html>")
    return "".join(html_lines)

def export_chat_to_pdf(chat_history) -> bytes:
    try:
        # Try to configure wkhtmltopdf - fallback to default if not found
        try:
            config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
        except:
            config = None
            
        html_content = render_chat_to_html(chat_history)
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(html_content)
            temp_html = f.name
        
        pdf_path = temp_html.replace(".html", ".pdf")
        
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'quiet': ''
        }
        
        try:
            if config:
                pdfkit.from_file(temp_html, pdf_path, configuration=config, options=options)
            else:
                pdfkit.from_file(temp_html, pdf_path, options=options)
                
            with open(pdf_path, "rb") as f:
                return f.read()
        finally:
            for path in [temp_html, pdf_path]:
                if os.path.exists(path):
                    os.remove(path)
    except Exception as e:
        logger.error(f"PDF export failed: {str(e)}")
        raise RuntimeError(f"Failed to export PDF: {str(e)}")