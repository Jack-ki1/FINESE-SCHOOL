"""
providers.py — dispatches an "ask the AI" request to whichever provider
and model the user picked in the sidebar, using their own API key.

Design goals:
  - No provider SDKs required, just `requests` — keeps the install light
    and avoids version conflicts between provider SDKs.
  - Every function has the same signature and same return shape, so the
    Flask route that calls this module doesn't need to know provider
    internals.
  - Keys are never stored: they arrive with the request and are used
    once, in memory, for that single call.
  - Local models (Ollama) need no key at all, which is the fully-offline
    AI path — everything else needs the user's own key and a live
    internet connection.
"""

from __future__ import annotations
import requests

TIMEOUT = 30  # seconds — a slow provider should fail loudly, not hang the page


class ProviderError(Exception):
    """Raised whenever a provider call fails, with a message safe to show the user."""


# ---------------------------------------------------------------------------
# Provider registry — feeds the sidebar's dropdowns on the frontend
# ---------------------------------------------------------------------------

PROVIDERS = {
    "gemini": {
        "label": "Google Gemini",
        "needs_key": True,
        "models": ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
    },
    "openai": {
        "label": "OpenAI",
        "needs_key": True,
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-4.1"],
    },
    "anthropic": {
        "label": "Anthropic",
        "needs_key": True,
        "models": ["claude-sonnet-4-6", "claude-haiku-4-5-20251001"],
    },
    "groq": {
        "label": "Groq",
        "needs_key": True,
        "models": ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
    },
    "mistral": {
        "label": "Mistral AI",
        "needs_key": True,
        "models": ["mistral-large-latest", "mistral-small-latest"],
    },
    "cohere": {
        "label": "Cohere",
        "needs_key": True,
        "models": ["command-r-plus", "command-r"],
    },
    "huggingface": {
        "label": "Hugging Face",
        "needs_key": True,
        "models": ["meta-llama/Llama-3.1-8B-Instruct", "mistralai/Mistral-7B-Instruct-v0.3"],
    },
    "ollama": {
        "label": "Ollama (local, offline)",
        "needs_key": False,
        "models": ["llama3.2", "mistral", "phi3", "qwen2.5"],
    },
}


def build_system_prompt(topic_name: str, subtopic_title: str | None, socratic: bool) -> str:
    """A short, topic-aware system prompt so the 'ask AI' panel stays on-task."""
    scope = f"{topic_name} — {subtopic_title}" if subtopic_title else topic_name
    base = (
        f"You are a precise, encouraging tutor helping a student studying {scope} on "
        "FINESE SCHOOL, a self-paced learning platform. Keep answers focused, use short "
        "code examples where useful, and connect back to the lesson content when relevant."
    )
    if socratic:
        base += (
            " Favor the Socratic method: ask one guiding question before giving the full "
            "answer, unless the student explicitly asks you to just tell them."
        )
    return base


# ---------------------------------------------------------------------------
# One function per provider — same signature, same return shape:
#   ask_<provider>(api_key, model, system_prompt, question) -> str
# ---------------------------------------------------------------------------

def ask_openai(api_key, model, system_prompt, question):
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            "max_tokens": 900,
        },
        timeout=TIMEOUT,
    )
    _raise_for_status(resp, "OpenAI")
    return resp.json()["choices"][0]["message"]["content"]


def ask_anthropic(api_key, model, system_prompt, question):
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "system": system_prompt,
            "max_tokens": 900,
            "messages": [{"role": "user", "content": question}],
        },
        timeout=TIMEOUT,
    )
    _raise_for_status(resp, "Anthropic")
    blocks = resp.json().get("content", [])
    return "".join(b.get("text", "") for b in blocks if b.get("type") == "text")


def ask_gemini(api_key, model, system_prompt, question):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    resp = requests.post(
        url,
        json={
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": question}]}],
        },
        timeout=TIMEOUT,
    )
    _raise_for_status(resp, "Google Gemini")
    data = resp.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise ProviderError("Gemini returned no candidates — the prompt may have been blocked.")
    parts = candidates[0]["content"]["parts"]
    return "".join(p.get("text", "") for p in parts)


def ask_groq(api_key, model, system_prompt, question):
    # Groq's API is OpenAI-compatible
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            "max_tokens": 900,
        },
        timeout=TIMEOUT,
    )
    _raise_for_status(resp, "Groq")
    return resp.json()["choices"][0]["message"]["content"]


def ask_mistral(api_key, model, system_prompt, question):
    resp = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
        },
        timeout=TIMEOUT,
    )
    _raise_for_status(resp, "Mistral AI")
    return resp.json()["choices"][0]["message"]["content"]


def ask_cohere(api_key, model, system_prompt, question):
    resp = requests.post(
        "https://api.cohere.com/v2/chat",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
        },
        timeout=TIMEOUT,
    )
    _raise_for_status(resp, "Cohere")
    data = resp.json()
    content = data.get("message", {}).get("content", [])
    return "".join(c.get("text", "") for c in content if c.get("type") == "text")


def ask_huggingface(api_key, model, system_prompt, question):
    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{model}",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"inputs": f"{system_prompt}\n\nStudent: {question}\nTutor:"},
        timeout=TIMEOUT,
    )
    _raise_for_status(resp, "Hugging Face")
    data = resp.json()
    if isinstance(data, list) and data and "generated_text" in data[0]:
        return data[0]["generated_text"]
    raise ProviderError("Hugging Face returned an unexpected response shape.")


def ask_ollama(api_key, model, system_prompt, question):
    # Local model — no API key, no internet required. `api_key` is unused
    # but kept in the signature so every provider function matches.
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": f"{system_prompt}\n\nStudent: {question}\nTutor:",
            "stream": False,
        },
        timeout=TIMEOUT,
    )
    _raise_for_status(resp, "Ollama (local)")
    return resp.json().get("response", "")


_DISPATCH = {
    "openai": ask_openai,
    "anthropic": ask_anthropic,
    "gemini": ask_gemini,
    "groq": ask_groq,
    "mistral": ask_mistral,
    "cohere": ask_cohere,
    "huggingface": ask_huggingface,
    "ollama": ask_ollama,
}


def ask(provider: str, api_key: str, model: str, system_prompt: str, question: str) -> str:
    """Single entry point the Flask route calls — routes to the right provider function."""
    if provider not in _DISPATCH:
        raise ProviderError(f"Unknown provider '{provider}'.")
    if PROVIDERS[provider]["needs_key"] and not api_key:
        raise ProviderError(f"{PROVIDERS[provider]['label']} needs an API key — add yours in the sidebar.")
    try:
        answer = _DISPATCH[provider](api_key, model, system_prompt, question)
    except requests.exceptions.Timeout:
        raise ProviderError(f"{PROVIDERS[provider]['label']} timed out after {TIMEOUT}s. Try again.")
    except requests.exceptions.ConnectionError:
        if provider == "ollama":
            raise ProviderError("Couldn't reach Ollama on localhost:11434 — is `ollama serve` running?")
        raise ProviderError(f"Couldn't reach {PROVIDERS[provider]['label']} — check your internet connection.")
    except ProviderError:
        raise
    except Exception as e:
        raise ProviderError(f"{PROVIDERS[provider]['label']} request failed: {e}")

    answer = (answer or "").strip()
    if not answer:
        raise ProviderError(f"{PROVIDERS[provider]['label']} returned an empty response.")
    return answer


def _raise_for_status(resp: requests.Response, provider_label: str):
    if resp.status_code == 401:
        raise ProviderError(f"{provider_label} rejected the API key (401). Double-check it in the sidebar.")
    if resp.status_code == 429:
        raise ProviderError(f"{provider_label} rate-limited this request (429). Wait a moment and retry.")
    if not resp.ok:
        raise ProviderError(f"{provider_label} error {resp.status_code}: {resp.text[:200]}")
