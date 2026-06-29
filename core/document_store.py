"""
DocumentStore - Handles uploaded files for RAG (Retrieval-Augmented Generation).
"""
import os
import pickle
import uuid
from typing import List, Dict, Optional
from datetime import datetime

DOC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'flask_session', 'docs')
os.makedirs(DOC_DIR, exist_ok=True)


class DocumentStore:
    """Store and retrieve uploaded documents per session."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self._filepath = os.path.join(DOC_DIR, f"{session_id}_docs.pkl")
        self._data = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self._filepath):
            try:
                with open(self._filepath, 'rb') as f:
                    return pickle.load(f)
            except Exception:
                pass
        return {'documents': []}
    
    def _save(self):
        with open(self._filepath, 'wb') as f:
            pickle.dump(self._data, f)
    
    def add_document(self, filename: str, content: str, doc_type: str = 'text') -> Dict:
        doc = {
            'id': str(uuid.uuid4()),
            'filename': filename,
            'content': content,
            'type': doc_type,
            'uploaded_at': datetime.now().isoformat(),
        }
        self._data['documents'].append(doc)
        self._save()
        return doc
    
    def get_documents(self) -> List[Dict]:
        return self._data['documents']
    
    def get_document(self, doc_id: str) -> Optional[Dict]:
        for doc in self._data['documents']:
            if doc['id'] == doc_id:
                return doc
        return None
    
    def delete_document(self, doc_id: str) -> bool:
        for i, doc in enumerate(self._data['documents']):
            if doc['id'] == doc_id:
                self._data['documents'].pop(i)
                self._save()
                return True
        return False
    
    def clear_all(self):
        self._data['documents'] = []
        self._save()
    
    def get_combined_context(self, max_chars: int = 8000) -> str:
        """Combine all document contents for RAG context."""
        combined = []
        total = 0
        for doc in self._data['documents']:
            header = "\n--- " + doc['filename'] + " ---\n"
            chunk = header + doc['content']
            if total + len(chunk) > max_chars:
                remaining = max_chars - total
                if remaining > 100:
                    combined.append(chunk[:remaining])
                break
            combined.append(chunk)
            total += len(chunk)
        return "\n".join(combined)