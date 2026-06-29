"""
Multi-provider LLM service with MCP (Model Context Protocol) support.
Supports OpenAI, Anthropic, Google, HuggingFace, and Ollama.
"""
import os
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ── Provider Imports ───────────────────────────────────────────────
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI library not installed. Run: pip install openai")

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("Anthropic library not installed. Run: pip install anthropic")

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    logger.warning("Google Generative AI library not installed. Run: pip install google-generativeai")

# ── MCP Support ──────────────────────────────────────────────────
try:
    from .mcp_service import configure_mcp_client, get_mcp_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    logger.info("MCP (Model Context Protocol) service not available.")


@dataclass
class LLMResponse:
    content: str
    usage: Optional[Dict[str, int]] = None
    model: Optional[str] = None
    provider: Optional[str] = None


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        pass
    
    @abstractmethod
    def available_models(self) -> List[str]:
        pass


class OpenAILLMProvider(BaseLLMProvider):
    """OpenAI-compatible LLM provider."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if not self.api_key and OPENAI_AVAILABLE:
            logger.warning("No OpenAI API key found. Set OPENAI_API_KEY environment variable.")
        
        if OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not installed. Run: pip install openai")
        
        if not self.api_key:
            raise ValueError("OpenAI API key not set")
        
        # Prepare the call parameters
        params = {
            'model': kwargs.get('model', 'gpt-4o-mini'),
            'messages': messages,
            'temperature': kwargs.get('temperature', 0.7),
            'max_tokens': kwargs.get('max_tokens', 1024),
        }
        
        # Include tools if MCP is available and requested
        if kwargs.get('use_tools', False) and MCP_AVAILABLE:
            mcp_client = get_mcp_client()
            if mcp_client:
                tool_definitions = mcp_client.get_tool_definitions()
                params['tools'] = tool_definitions
                params['tool_choice'] = "auto"  # Let the model decide when to use tools
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        try:
            response = self.client.chat.completions.create(**params)
            
            # Handle tool calls if present
            if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
                # Execute tools and get results
                tool_results = []
                for tool_call in response.choices[0].message.tool_calls:
                    # Parse the arguments
                    import json
                    try:
                        args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        args = {}
                    
                    # Execute the tool call using MCP client
                    mcp_client = get_mcp_client()
                    if mcp_client:
                        result = mcp_client.execute_tool_call(tool_call.function.name, args)
                        tool_results.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": tool_call.function.name,
                            "content": str(result)
                        })
                
                # If we have tool results, call again with results to get final response
                if tool_results:
                    new_messages = messages + [response.choices[0].message.model_dump()] + tool_results
                    
                    # Make a second call with tool results
                    final_params = {
                        'model': params['model'],
                        'messages': new_messages,
                        'temperature': params['temperature'],
                        'max_tokens': params['max_tokens'],
                    }
                    final_response = self.client.chat.completions.create(**final_params)
                    content = final_response.choices[0].message.content
                else:
                    content = response.choices[0].message.content
            else:
                content = response.choices[0].message.content
            
            return LLMResponse(
                content=content,
                usage={
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens,
                } if response.usage else None,
                model=response.model,
                provider='openai'
            )
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def available_models(self) -> List[str]:
        if not OPENAI_AVAILABLE:
            return []
        
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception:
            return ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo']


class AnthropicLLMProvider(BaseLLMProvider):
    """Anthropic Claude provider."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key and ANTHROPIC_AVAILABLE:
            logger.warning("No Anthropic API key found. Set ANTHROPIC_API_KEY environment variable.")
        
        if ANTHROPIC_AVAILABLE:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic library not installed. Run: pip install anthropic")
        
        if not self.api_key:
            raise ValueError("Anthropic API key not set")
        
        # Convert messages from OpenAI format to Anthropic format
        # Anthropic requires alternating human/assistant messages
        formatted_messages = []
        for msg in messages:
            if msg['role'] == 'system':
                # Anthropic handles system messages differently
                continue  # Skip system message here, add separately
            elif msg['role'] == 'user':
                formatted_messages.append({"role": "user", "content": msg['content']})
            elif msg['role'] == 'assistant':
                formatted_messages.append({"role": "assistant", "content": msg['content']})
        
        params = {
            'model': kwargs.get('model', 'claude-3-haiku-20240307'),
            'messages': formatted_messages,
            'temperature': kwargs.get('temperature', 0.7),
            'max_tokens': kwargs.get('max_tokens', 1024),
        }
        
        # Add tools if MCP is available and requested
        if MCP_AVAILABLE and kwargs.get('enable_tools', False):
            from .mcp_service import get_mcp_client
            mcp_client = get_mcp_client()
            params['tools'] = mcp_client.get_tool_definitions()
        
        # Add system message separately if present
        system_msg = None
        for msg in messages:
            if msg['role'] == 'system':
                system_msg = msg['content']
                break
        
        if system_msg:
            params['system'] = system_msg
            
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        try:
            response = self.client.messages.create(**params)
            
            # Handle tool calls if present
            content = response.content[0].text if response.content else ""
            
            return LLMResponse(
                content=content,
                usage={
                    'prompt_tokens': response.usage.input_tokens,
                    'completion_tokens': response.usage.output_tokens,
                    'total_tokens': response.usage.input_tokens + response.usage.output_tokens,
                },
                model=response.model,
                provider='anthropic'
            )
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    def available_models(self) -> List[str]:
        if ANTHROPIC_AVAILABLE:
            return ['claude-3-haiku-20240307', 'claude-3-sonnet-20240229', 'claude-3-opus-20240229']
        return []


class GoogleLLMProvider(BaseLLMProvider):
    """Google Gemini provider."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('GOOGLE_API_KEY')
        if not self.api_key and GOOGLE_AVAILABLE:
            logger.warning("No Google API key found. Set GOOGLE_API_KEY environment variable.")
        
        if GOOGLE_AVAILABLE:
            genai.configure(api_key=self.api_key)
        else:
            self.model = None
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        if not GOOGLE_AVAILABLE:
            raise ImportError("Google Generative AI library not installed. Run: pip install google-generativeai")
        
        if not self.api_key:
            raise ValueError("Google API key not set")
        
        model_name = kwargs.get('model', 'gemini-1.5-flash')
        self.model = genai.GenerativeModel(model_name)
        
        # Convert messages to Google format
        # Google expects a single conversation with alternating user/assistant parts
        converted_history = []
        current_user_content = ""
        
        for msg in messages:
            if msg['role'] == 'system':
                # Google handles system instructions differently
                continue  # We'll handle system message separately
            elif msg['role'] == 'user':
                current_user_content = msg['content']
            elif msg['role'] == 'assistant':
                if current_user_content:
                    converted_history.append({'role': 'user', 'parts': [current_user_content]})
                    current_user_content = ""
                converted_history.append({'role': 'model', 'parts': [msg['content']]})
        
        # Add remaining user message if exists
        if current_user_content:
            converted_history.append({'role': 'user', 'parts': [current_user_content]})
        
        # Create chat session with history
        chat = self.model.start_chat(history=converted_history)
        
        # Prepare generation config
        generation_config = {
            'temperature': kwargs.get('temperature', 0.7),
            'max_output_tokens': kwargs.get('max_tokens', 1024),
        }
        
        # Get system instruction if exists
        system_instruction = None
        for msg in messages:
            if msg['role'] == 'system':
                system_instruction = msg['content']
                break
        
        try:
            if system_instruction:
                # For system instructions, we'll add it to the prompt
                response = chat.send_message(
                    system_instruction + "\n\n" + (messages[-1]['content'] if messages else ""),
                    generation_config=generation_config
                )
            else:
                response = chat.send_message(
                    messages[-1]['content'] if messages else "Hello",
                    generation_config=generation_config
                )
            
            return LLMResponse(
                content=response.text,
                usage=None,  # Google doesn't provide usage in the same way
                model=model_name,
                provider='google'
            )
        except Exception as e:
            logger.error(f"Google API error: {e}")
            raise
    
    def available_models(self) -> List[str]:
        if GOOGLE_AVAILABLE:
            try:
                models = genai.list_models()
                return [model.name.replace("models/", "") for model in models]
            except Exception:
                return ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro']
        return []


class HuggingFaceLLMProvider(BaseLLMProvider):
    """Hugging Face Inference API provider."""
    
    def __init__(self, hf_token: str = None):
        self.hf_token = hf_token or os.environ.get('HF_TOKEN')
        if not self.hf_token:
            logger.warning("No Hugging Face token found. Set HF_TOKEN environment variable.")
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        import requests
        
        model = kwargs.get('model', 'mistralai/Mistral-7B-Instruct-v0.3')
        api_url = f"https://api-inference.huggingface.co/models/{model}"
        
        if not self.hf_token:
            raise ValueError("Hugging Face token not set")
        
        # Format messages for HuggingFace
        # Using chat template approach
        prompt = ""
        for msg in messages:
            role = msg['role']
            content = msg['content']
            if role == 'user':
                prompt += f"[INST] {content} [/INST]"
            elif role == 'assistant':
                prompt += f" {content} "
            elif role == 'system':
                prompt = f"<<SYS>> {content} <</SYS>> {prompt}" if prompt else f"<<SYS>> {content} <</SYS>>\n"
        
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": kwargs.get('temperature', 0.7),
                "max_new_tokens": kwargs.get('max_tokens', 1024),
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            content = result[0]['generated_text']
            
            return LLMResponse(
                content=content,
                provider='huggingface'
            )
        except Exception as e:
            logger.error(f"Hugging Face API error: {e}")
            raise
    
    def available_models(self) -> List[str]:
        return ['mistralai/Mistral-7B-Instruct-v0.3', 'google/gemma-7b-it', 'meta-llama/Llama-2-7b-chat-hf']


class OllamaLLMProvider(BaseLLMProvider):
    """Local Ollama provider."""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        import requests
        
        model = kwargs.get('model', 'llama3.2')
        url = f"{self.base_url}/api/chat"
        
        payload = {
            'model': model,
            'messages': messages,
            'options': {
                'temperature': kwargs.get('temperature', 0.7),
                'num_predict': kwargs.get('max_tokens', 1024),
            },
            'stream': False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            return LLMResponse(
                content=result['message']['content'],
                usage=None,  # Ollama doesn't always provide detailed usage
                model=result.get('model'),
                provider='ollama'
            )
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise
    
    def available_models(self) -> List[str]:
        import requests
        
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
        except Exception:
            pass
        
        return ['llama3.2', 'mistral', 'gemma:7b', 'phi3']


class LLMService:
    """Main LLM service with multi-provider support and MCP capabilities."""
    
    def __init__(self):
        self.providers = {
            'openai': OpenAILLMProvider(),
            'anthropic': AnthropicLLMProvider(),
            'google': GoogleLLMProvider(),
            'huggingface': HuggingFaceLLMProvider(),
            'ollama': OllamaLLMProvider(),
        }
    
    @classmethod
    def get_provider(cls, provider_name: str, model: str = None):
        """Get an instance of the specified provider."""
        service = cls()
        if provider_name not in service.providers:
            raise ValueError(f"Unsupported provider: {provider_name}")
        
        return service.providers[provider_name]
    
    @classmethod
    def available_providers(cls) -> Dict[str, bool]:
        """Check which providers are available based on installed libraries and API keys."""
        service = cls()
        available = {}
        
        checks = {
            'openai': lambda: bool(service.providers['openai'].api_key) and OPENAI_AVAILABLE,
            'anthropic': lambda: bool(service.providers['anthropic'].api_key) and ANTHROPIC_AVAILABLE,
            'google': lambda: bool(service.providers['google'].api_key) and GOOGLE_AVAILABLE,
            'huggingface': lambda: bool(service.providers['huggingface'].hf_token),
            'ollama': lambda: True,  # Ollama is local, always potentially available
        }
        
        for name, check in checks.items():
            try:
                available[name] = check()
            except Exception:
                available[name] = False
                
        return available
    
    @classmethod
    def get_mcp_client(cls):
        """Initialize and return an MCP client if available."""
        if not MCP_AVAILABLE:
            logger.warning("MCP not available. Install with: pip install mcp")
            return None
        
        try:
            # Import and return the MCP client
            return get_mcp_client()
        except Exception as e:
            logger.error(f"Error initializing MCP client: {e}")
            return None


# ── Socratic Mode Helper ──────────────────────────────────────────
def create_socratic_prompt(question: str, subject_area: str = "general") -> str:
    """
    Creates a prompt that encourages Socratic questioning approach.
    Instead of giving direct answers, guides the student to discover solutions.
    """
    socratic_system = f"""
You are an expert tutor using the Socratic method. Your role is to guide students to discover answers themselves through thoughtful questions, rather than providing direct solutions.

Guidelines:
1. Ask leading questions that guide the student toward the solution
2. Break complex problems into smaller, manageable questions
3. Encourage critical thinking by asking "what if" or "how do you think" questions
4. If the student makes an error, ask them to reconsider their approach rather than correcting directly
5. Acknowledge good thinking and encourage further exploration
6. Adapt your questions to the subject area: {subject_area}

Remember: Your goal is to promote understanding, not just get the right answer.
"""
    
    return socratic_system


# ── Adaptive Difficulty Helper ───────────────────────────────────
def calculate_difficulty_score(user_performance: List[bool], recent_streak: int = 0) -> str:
    """
    Calculate adaptive difficulty level based on user performance.
    Returns 'beginner', 'intermediate', or 'advanced'.
    """
    if not user_performance:
        return 'beginner'
    
    accuracy = sum(user_performance) / len(user_performance)
    
    # Adjust based on both accuracy and recent streak
    if accuracy >= 0.8 and recent_streak >= 2:
        return 'advanced'
    elif accuracy >= 0.6:
        return 'intermediate'
    else:
        return 'beginner'


# ── Multi-Model Routing Helper ───────────────────────────────────
def select_model_by_task(task_complexity: str, task_type: str, available_providers: Dict[str, bool]):
    """
    Select the appropriate model based on task requirements.
    Implements the 80/20 rule: heavy tasks to big models, simple to mini models.
    """
    routing_rules = {
        ('complex', 'reasoning'): ['openai:gpt-4o', 'anthropic:claude-3-sonnet-20240229'],
        ('complex', 'analysis'): ['openai:gpt-4o', 'anthropic:claude-3-sonnet-20240229'],
        ('simple', 'factoid'): ['openai:gpt-4o-mini', 'anthropic:claude-3-haiku-20240307'],
        ('simple', 'qa'): ['openai:gpt-4o-mini', 'anthropic:claude-3-haiku-20240307'],
        ('medium', 'coding'): ['openai:gpt-4o', 'google:gemini-1.5-pro'],
        ('medium', 'explanation'): ['anthropic:claude-3-sonnet-20240229', 'google:gemini-1.5-flash'],
        ('complex', 'data_analysis'): ['openai:gpt-4o', 'google:gemini-1.5-pro'],
        ('simple', 'data_query'): ['openai:gpt-4o-mini', 'anthropic:claude-3-haiku-20240307'],
    }
    
    key = (task_complexity, task_type)
    candidates = routing_rules.get(key, ['openai:gpt-4o-mini', 'anthropic:claude-3-haiku-20240307'])
    
    # Filter by available providers
    for candidate in candidates:
        provider = candidate.split(':')[0]
        if available_providers.get(provider, False):
            return candidate
    
    # Fallback to default
    return 'openai:gpt-4o-mini'


# ── Enhanced LLM Service with MCP Integration ────────────────────
def get_optimized_provider(task_description: str, use_mcp: bool = False):
    """
    Get the most appropriate provider based on task description and MCP availability.
    """
    # Determine task complexity and type
    task_complexity = 'simple'
    task_type = 'qa'
    
    if any(keyword in task_description.lower() for keyword in ['analyze', 'compare', 'evaluate']):
        task_complexity = 'complex'
        task_type = 'analysis'
    elif any(keyword in task_description.lower() for keyword in ['code', 'program', 'function']):
        task_complexity = 'medium'
        task_type = 'coding'
    elif any(keyword in task_description.lower() for keyword in ['data', 'sql', 'query']):
        task_complexity = 'medium'
        task_type = 'data_query'
    
    available_providers = LLMService.available_providers()
    selected_model = select_model_by_task(task_complexity, task_type, available_providers)
    provider_name, model_name = selected_model.split(':', 1) if ':' in selected_model else ('openai', 'gpt-4o-mini')
    
    provider = LLMService.get_provider(provider_name, model_name)
    
    # Add MCP tools if requested and available
    if use_mcp and MCP_AVAILABLE:
        # Return provider with MCP configuration
        return provider, {'use_tools': True}
    else:
        return provider, {}
