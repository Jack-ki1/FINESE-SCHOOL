"""
ChatStore - Server-side chat history persistence using pickle.
Handles multiple conversations per user session.
"""
import pickle
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional

CHAT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'flask_session', 'chats')
os.makedirs(CHAT_DIR, exist_ok=True)


class ChatStore:
    """Persistent chat storage using pickle files."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self._filepath = os.path.join(CHAT_DIR, f"{session_id}.pkl")
        self._data = self._load()
    
    def _load(self) -> Dict:
        """Load chat data from disk or return defaults."""
        if os.path.exists(self._filepath):
            try:
                with open(self._filepath, 'rb') as f:
                    return pickle.load(f)
            except Exception:
                pass
        return {
            'conversations': {},
            'active_conversation_id': None,
            'settings': {
                'provider': 'openai',
                'model': 'gpt-4o-mini',
                'temperature': 0.7,
                'max_tokens': 1024,
                'system_message': 'You are a helpful, friendly AI assistant.',
            }
        }
    
    def _save(self):
        """Persist chat data to disk."""
        with open(self._filepath, 'wb') as f:
            pickle.dump(self._data, f)
    
    # ---- Conversations ----
    
    def create_conversation(self, title: str = "New Chat") -> str:
        """Create a new conversation and return its ID."""
        conv_id = str(uuid.uuid4())
        self._data['conversations'][conv_id] = {
            'id': conv_id,
            'title': title,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'messages': [],
        }
        self._data['active_conversation_id'] = conv_id
        self._save()
        return conv_id
    
    def get_conversation(self, conv_id: str) -> Optional[Dict]:
        """Get a conversation by ID."""
        return self._data['conversations'].get(conv_id)
    
    def get_all_conversations(self) -> List[Dict]:
        """Get all conversations sorted by updated_at desc."""
        convs = list(self._data['conversations'].values())
        convs.sort(key=lambda x: x['updated_at'], reverse=True)
        return convs
    
    def delete_conversation(self, conv_id: str) -> bool:
        """Delete a conversation."""
        if conv_id in self._data['conversations']:
            del self._data['conversations'][conv_id]
            if self._data['active_conversation_id'] == conv_id:
                remaining = list(self._data['conversations'].keys())
                self._data['active_conversation_id'] = remaining[0] if remaining else None
            self._save()
            return True
        return False
    
    def rename_conversation(self, conv_id: str, new_title: str) -> bool:
        """Rename a conversation."""
        conv = self._data['conversations'].get(conv_id)
        if conv:
            conv['title'] = new_title
            conv['updated_at'] = datetime.now().isoformat()
            self._save()
            return True
        return False
    
    def set_active_conversation(self, conv_id: str) -> bool:
        """Set the active conversation."""
        if conv_id in self._data['conversations']:
            self._data['active_conversation_id'] = conv_id
            self._save()
            return True
        return False
    
    def get_active_conversation(self) -> Optional[Dict]:
        """Get the currently active conversation."""
        conv_id = self._data.get('active_conversation_id')
        if conv_id:
            return self._data['conversations'].get(conv_id)
        return None
    
    def get_active_conversation_id(self) -> Optional[str]:
        return self._data.get('active_conversation_id')
    
    # ---- Messages ----
    
    def add_message(self, conv_id: str, role: str, content: str, metadata: Dict = None) -> Dict:
        """Add a message to a conversation."""
        conv = self._data['conversations'].get(conv_id)
        if not conv:
            return None
        
        msg = {
            'id': str(uuid.uuid4()),
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {},
        }
        conv['messages'].append(msg)
        conv['updated_at'] = datetime.now().isoformat()
        
        # Auto-title first user message
        if role == 'user' and len(conv['messages']) == 1:
            conv['title'] = content[:40] + ('...' if len(content) > 40 else '')
        
        self._save()
        return msg
    
    def get_messages(self, conv_id: str) -> List[Dict]:
        """Get all messages for a conversation."""
        conv = self._data['conversations'].get(conv_id)
        return conv['messages'] if conv else []
    
    def clear_messages(self, conv_id: str) -> bool:
        """Clear all messages in a conversation."""
        conv = self._data['conversations'].get(conv_id)
        if conv:
            conv['messages'] = []
            conv['updated_at'] = datetime.now().isoformat()
            self._save()
            return True
        return False
    
    # ---- Settings ----
    
    def get_settings(self) -> Dict:
        return self._data.get('settings', {})
    
    def update_settings(self, **kwargs) -> Dict:
        self._data['settings'].update(kwargs)
        self._save()
        return self._data['settings']
    
    def reset_settings(self):
        self._data['settings'] = {
            'provider': 'openai',
            'model': 'gpt-4o-mini',
            'temperature': 0.7,
            'max_tokens': 1024,
            'system_message': 'You are a helpful, friendly AI assistant.',
        }
        self._save()