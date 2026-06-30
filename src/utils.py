import re
import html
import uuid
import logging
from typing import List, Tuple, Optional

# Configure logging
logger = logging.getLogger(__name__)

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent potential injection attacks.
    
    Args:
        text: User input text
        
    Returns:
        Sanitized text with safe characters only
    """
    try:
        # Remove any potentially harmful characters while preserving basic formatting
        sanitized = re.sub(r'[<>]', '', text)
        # Remove any JavaScript event handlers
        sanitized = re.sub(r'on\w+="[^"]*"', '', sanitized, flags=re.IGNORECASE)
        # Limit length with increased capacity
        return sanitized[:2000]
    except Exception as e:
        logger.error(f"Error sanitizing input: {e}")
        return ""

def strip_html(text: str) -> str:
    """Remove HTML tags from text while preserving content structure.
    
    Args:
        text: HTML content to be stripped
        
    Returns:
        Plain text with HTML tags removed but content structure preserved
    """
    if not text:
        return ""
        
    # Replace line break tags with actual line breaks
    text = text.replace('<br>', '\n')
    text = text.replace('<br/>', '\n')
    text = text.replace('</p>', '\n\n')
    text = text.replace('</div>', '\n\n')
    
    # Replace list tags with appropriate formatting
    text = re.sub(r'</?ul>', '\n', text)
    text = re.sub(r'</?ol>', '\n', text)
    text = re.sub(r'<li>', '\n- ', text)
    
    # Remove remaining HTML tags
    clean_text = re.sub(r"<[^>]+>", "", text)
    
    # Clean up extra whitespace
    clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)
    return clean_text.strip()

def inject_interactive_elements(html_str: str) -> str:
    """
    Add interactive elements to HTML content like:
    - Copy buttons for code blocks
    - Expandable sections for long content
    - Syntax highlighting
    
    Args:
        html_str: HTML content with potential code blocks
        
    Returns:
        HTML content with interactive elements added
    """
    if not html_str or '```' not in html_str:
        return html_str
        
    import re
    
    # Add copy buttons to code blocks
    def add_copy_button(match):
        code_content = match.group(2)
        code_lang = match.group(1) if match.group(1) else "text"
        button_id = str(uuid.uuid4())[:8]
        
        return f'''
        <div style="position: relative; margin: 10px 0;">
            <button id="copy-btn-{button_id}" onclick="copyCode('{button_id}')" 
                style="position: absolute; top: 5px; right: 5px; z-index: 10; 
                       background: #f0f0f0; border: 1px solid #ccc; border-radius: 4px; 
                       padding: 4px 8px; cursor: pointer; font-size: 12px;">
                Copy
            </button>
            <pre style="padding: 20px 10px 10px 10px; border-radius: 8px; 
                        background: #f8f8f8; overflow-x: auto; position: relative;">
                <code class="language-{code_lang}">{html.escape(code_content)}</code>
            </pre>
        </div>
        '''
    
    # Process code blocks with language specification
    try:
        result = re.sub(r'```(\w*)\n(.*?)```', add_copy_button, html_str, flags=re.DOTALL)
        
        # Add JavaScript for copy functionality
        js_script = """
        <script>
        function copyCode(elementId) {
            const button = document.getElementById('copy-btn-' + elementId);
            const codeBlock = button.nextElementSibling.querySelector('code');
            const text = codeBlock.textContent;
            
            navigator.clipboard.writeText(text).then(() => {
                const originalText = button.textContent;
                button.textContent = 'Copied!';
                setTimeout(() => {
                    button.textContent = originalText;
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy: ', err);
                button.textContent = 'Failed';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 2000);
            });
        }
        
        // Initialize syntax highlighting
        document.addEventListener('DOMContentLoaded', (event) => {
            document.querySelectorAll('pre code').forEach((el) => {
                hljs.highlightElement(el);
            });
        });
        </script>
        """
        
        # Add syntax highlighting CSS if needed
        css_link = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/github.min.css">\n'
        hljs_script = '<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>\n'
        
        # Add the script and CSS if we have code blocks
        result = css_link + hljs_script + result + js_script
        
        return result
    except Exception as e:
        logger.error(f"Error adding interactive elements: {e}")
        return html_str

def detect_language_from_context(question: str, topic: str) -> str:
    """Detect the programming language based on question and topic context.
    
    Args:
        question: User's question text
        topic: Main topic of the query
        
    Returns:
        Detected programming language code
    """
    # Language mapping with common indicators
    mapping = {
        "Python": ["python", "pandas", "numpy", "matplotlib", "dataframe"],
        "SQL": ["sql", "query", "database", "select", "join"],
        "JavaScript": ["javascript", "js", "react", "dom", "node"],
        "Java": ["java", "spring", "hibernate"],
        "C#": ["c#", "csharp", "dotnet", ".net"],
        "Power BI": ["dax", "powerbi", "power bi", "pbix"],
        "Data Visualization": ["visualization", "chart", "plot", "graph"],
        "HTML": ["html", "markup", "webpage"],
        "CSS": ["css", "stylesheet"],
        "Shell": ["bash", "shell", "command", "script"]
    }
    
    # Check topic first with exact matches
    for lang, keywords in mapping.items():
        for keyword in keywords:
            if keyword.lower() in topic.lower():
                return lang.lower()
    
    # Check question for additional clues
    question_lower = question.lower()
    for lang, keywords in mapping.items():
        for keyword in keywords:
            if keyword.lower() in question_lower:
                return lang.lower()
    
    return "text"

def truncate_text(text: str, max_length: int = 500, min_length: int = 200) -> str:
    """Truncate text to a maximum length while trying to preserve meaningful content.
    
    Args:
        text: Text to truncate
        max_length: Maximum length for the truncated text
        min_length: Minimum length before adding ellipsis
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if not text:
        return ""
        
    if len(text) <= max_length:
        return text
        
    # Try to find a natural break point
    space_index = text.rfind(' ', min_length, max_length)
    if space_index > 0:
        return text[:space_index] + "..."
    
    # Fallback to simple truncation
    return text[:max_length] + "..."