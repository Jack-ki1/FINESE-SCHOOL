"""
LLM Service - Multi-provider language model integration.
Supports OpenAI, Anthropic, Google Gemini, Hugging Face Inference, and Ollama (local).
"""
import os
import json
import requests
from typing import List, Dict, Optional, Generator
from dataclasses import dataclass


@dataclass
class LLMResponse:
    content: str
    model: str
    provider: str
    usage: Dict = None
    metadata: Dict = None


class BaseLLMProvider:
    """Base class for LLM providers."""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key
        self.model = model
    
    def chat(self, messages: List[Dict], **kwargs) -> LLMResponse:
        raise NotImplementedError
    
    def chat_stream(self, messages: List[Dict], **kwargs) -> Generator[str, None, None]:
        """Stream response tokens. Default falls back to non-streaming."""
        response = self.chat(messages, **kwargs)
        yield response.content


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider."""
    
    def __init__(self, api_key: str = None, model: str = 'gpt-4o-mini'):
        super().__init__(api_key or os.environ.get('OPENAI_API_KEY', ''), model)
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            self.client = None
    
    def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1024, **kwargs) -> LLMResponse:
        if not self.client:
            raise RuntimeError("OpenAI package not installed. Run: pip install openai")
        if not self.api_key:
            raise RuntimeError("OpenAI API key not configured.")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return LLMResponse(
            content=response.choices[0].message.content,
            model=self.model,
            provider='openai',
            usage={
                'prompt_tokens': response.usage.prompt_tokens,
                'completion_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            }
        )
    
    def chat_stream(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1024, **kwargs):
        if not self.client:
            raise RuntimeError("OpenAI package not installed.")
        
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            **kwargs
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider."""
    
    def __init__(self, api_key: str = None, model: str = 'claude-3-haiku-20240307'):
        super().__init__(api_key or os.environ.get('ANTHROPIC_API_KEY', ''), model)
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            self.client = None
    
    def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1024, system: str = None, **kwargs) -> LLMResponse:
        if not self.client:
            raise RuntimeError("Anthropic package not installed. Run: pip install anthropic")
        if not self.api_key:
            raise RuntimeError("Anthropic API key not configured.")
        
        # Separate system message
        system_msg = system or ""
        chat_messages = [m for m in messages if m['role'] != 'system']
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_msg,
            messages=chat_messages,
            **kwargs
        )
        return LLMResponse(
            content=response.content[0].text,
            model=self.model,
            provider='anthropic',
            usage={
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens,
            }
        )
    
    def chat_stream(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1024, system: str = None, **kwargs):
        if not self.client:
            raise RuntimeError("Anthropic package not installed.")
        
        system_msg = system or ""
        chat_messages = [m for m in messages if m['role'] != 'system']
        
        with self.client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_msg,
            messages=chat_messages,
            **kwargs
        ) as stream:
            for text in stream.text_stream:
                yield text


class GoogleProvider(BaseLLMProvider):
    """Google Gemini provider."""
    
    def __init__(self, api_key: str = None, model: str = 'gemini-1.5-flash'):
        super().__init__(api_key or os.environ.get('GOOGLE_API_KEY', ''), model)
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.genai = genai
            self.model_obj = genai.GenerativeModel(self.model)
        except ImportError:
            self.genai = None
            self.model_obj = None
    
    def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1024, **kwargs) -> LLMResponse:
        if not self.genai:
            raise RuntimeError("Google Generative AI package not installed. Run: pip install google-generativeai")
        if not self.api_key:
            raise RuntimeError("Google API key not configured.")
        
        # Convert messages to Gemini format
        system_msg = ""
        history = []
        for m in messages:
            if m['role'] == 'system':
                system_msg = m['content']
            elif m['role'] == 'user':
                history.append({'role': 'user', 'parts': [m['content']]})
            elif m['role'] == 'assistant':
                history.append({'role': 'model', 'parts': [m['content']]})
        
        model = self.genai.GenerativeModel(
            self.model,
            system_instruction=system_msg if system_msg else None
        )
        chat = model.start_chat(history=history[:-1] if len(history) > 1 else [])
        
        response = chat.send_message(
            history[-1]['parts'][0] if history else "Hello",
            generation_config=self.genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
        )
        return LLMResponse(
            content=response.text,
            model=self.model,
            provider='google',
        )


class HuggingFaceProvider(BaseLLMProvider):
    """Hugging Face Inference API provider."""
    
    def __init__(self, api_key: str = None, model: str = 'mistralai/Mistral-7B-Instruct-v0.3'):
        super().__init__(api_key or os.environ.get('HF_TOKEN', ''), model)
    
    def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1024, **kwargs) -> LLMResponse:
        if not self.api_key:
            raise RuntimeError("Hugging Face token (HF_TOKEN) not configured.")
        
        # Build prompt from messages
        prompt = self._build_prompt(messages)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "return_full_text": False,
            }
        }
        
        api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        response = requests.post(api_url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            text = result[0].get('generated_text', '')
        else:
            text = str(result)
        
        return LLMResponse(
            content=text.strip(),
            model=self.model,
            provider='huggingface',
        )
    
    def _build_prompt(self, messages: List[Dict]) -> str:
        """Build a prompt string from message history."""
        parts = []
        for m in messages:
            if m['role'] == 'system':
                parts.append(f"[SYSTEM] {m['content']}[/SYSTEM]")
            elif m['role'] == 'user':
                parts.append(f"[INST] {m['content']} [/INST]")
            elif m['role'] == 'assistant':
                parts.append(m['content'])
        return "\n".join(parts)


class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider."""
    
    def __init__(self, api_key: str = None, model: str = 'llama3.2', base_url: str = 'http://localhost:11434'):
        super().__init__(api_key, model)
        self.base_url = base_url.rstrip('/')
    
    def chat(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1024, **kwargs) -> LLMResponse:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        
        response = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=300)
        response.raise_for_status()
        result = response.json()
        
        return LLMResponse(
            content=result.get('message', {}).get('content', ''),
            model=self.model,
            provider='ollama',
        )
    
    def chat_stream(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1024, **kwargs):
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        
        response = requests.post(f"{self.base_url}/api/chat", json=payload, stream=True, timeout=300)
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    if 'message' in data and 'content' in data['message']:
                        yield data['message']['content']
                except json.JSONDecodeError:
                    pass


class LLMService:
    """Unified LLM service that routes to the correct provider."""
    
    PROVIDERS = {
        'openai': OpenAIProvider,
        'anthropic': AnthropicProvider,
        'google': GoogleProvider,
        'huggingface': HuggingFaceProvider,
        'ollama': OllamaProvider,
    }
    
    DEFAULT_MODELS = {
        'openai': 'gpt-4o-mini',
        'anthropic': 'claude-3-haiku-20240307',
        'google': 'gemini-1.5-flash',
        'huggingface': 'mistralai/Mistral-7B-Instruct-v0.3',
        'ollama': 'llama3.2',
    }
    
    @classmethod
    def get_provider(cls, provider_name: str, model: str = None, api_key: str = None):
        provider_class = cls.PROVIDERS.get(provider_name)
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_name}. Available: {list(cls.PROVIDERS.keys())}")
        
        if not model:
            model = cls.DEFAULT_MODELS.get(provider_name)
        
        return provider_class(api_key=api_key, model=model)
    
    @classmethod
    def get_available_providers(cls) -> List[Dict]:
        """Return list of available providers with their status."""
        providers = []
        for name, pclass in cls.PROVIDERS.items():
            status = 'available'
            # Check if package is installed
            try:
                if name == 'openai':
                    import openai
                elif name == 'anthropic':
                    import anthropic
                elif name == 'google':
                    import google.generativeai
                elif name == 'ollama':
                    requests.get('http://localhost:11434', timeout=2)
            except Exception:
                status = 'package_missing' if name != 'ollama' else 'server_offline'
            
            # Check API key
            key_env = {
                'openai': 'OPENAI_API_KEY',
                'anthropic': 'ANTHROPIC_API_KEY',
                'google': 'GOOGLE_API_KEY',
                'huggingface': 'HF_TOKEN',
                'ollama': None,
            }
            has_key = bool(os.environ.get(key_env.get(name, ''), '')) if key_env.get(name) else True
            
            providers.append({
                'name': name,
                'default_model': cls.DEFAULT_MODELS.get(name),
                'status': status,
                'has_key': has_key,
            })
        return providers