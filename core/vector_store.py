"""
Vector Store - RAG (Retrieval-Augmented Generation) with ChromaDB.
Handles document chunking, embedding, and semantic search.
"""
import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB-based vector store for document RAG."""

    def __init__(self, persist_directory: str = None):
        self.persist_directory = persist_directory or os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'data', 'vectordb'
        )
        os.makedirs(self.persist_directory, exist_ok=True)
        self._client = None
        self._embedding_fn = None
        self._initialized = False

    def _ensure_initialized(self):
        """Lazy initialization of ChromaDB."""
        if self._initialized:
            return
        try:
            import chromadb
            self._client = chromadb.PersistentClient(path=self.persist_directory)
            self._initialized = True
            logger.info(f"ChromaDB initialized at {self.persist_directory}")
        except ImportError:
            logger.warning("ChromaDB not installed. RAG features disabled. Install: pip install chromadb")
            self._initialized = False

    def _get_collection(self, session_id: str):
        """Get or create a ChromaDB collection for a session."""
        self._ensure_initialized()
        if not self._client:
            return None
        return self._client.get_or_create_collection(
            name=f"session_{session_id}",
            metadata={"description": f"Documents for session {session_id}"}
        )

    def add_document(self, session_id: str, doc_id: str, text: str,
                     metadata: Dict = None, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Chunk a document and add to the vector store."""
        collection = self._get_collection(session_id)
        if not collection:
            return {'success': False, 'error': 'Vector store not available'}

        chunks = self._chunk_text(text, chunk_size, chunk_overlap)
        if not chunks:
            return {'success': False, 'error': 'No content to index'}

        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {**(metadata or {}), 'doc_id': doc_id, 'chunk_index': i, 'total_chunks': len(chunks)}
            for i in range(len(chunks))
        ]

        collection.add(documents=chunks, ids=ids, metadatas=metadatas)
        return {'success': True, 'chunks_added': len(chunks)}

    def search(self, session_id: str, query: str, n_results: int = 5) -> List[Dict]:
        """Search for relevant document chunks."""
        collection = self._get_collection(session_id)
        if not collection:
            return []

        try:
            results = collection.query(query_texts=[query], n_results=n_results)
            chunks = []
            if results and results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    meta = results['metadatas'][0][i] if results['metadatas'] else {}
                    chunks.append({
                        'content': doc,
                        'metadata': meta,
                        'distance': results['distances'][0][i] if results.get('distances') else None,
                    })
            return chunks
        except Exception as e:
            logger.error(f"Vector search error: {e}")
            return []

    def delete_document(self, session_id: str, doc_id: str):
        """Remove all chunks for a document."""
        collection = self._get_collection(session_id)
        if not collection:
            return False
        try:
            # Get all chunks with this doc_id
            results = collection.get(where={"doc_id": doc_id})
            if results and results['ids']:
                collection.delete(ids=results['ids'])
            return True
        except Exception as e:
            logger.error(f"Delete error: {e}")
            return False

    def clear_session(self, session_id: str):
        """Remove all data for a session."""
        self._ensure_initialized()
        if not self._client:
            return
        try:
            self._client.delete_collection(f"session_{session_id}")
        except Exception:
            pass

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks."""
        if not text or not text.strip():
            return []

        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = start + chunk_size
            if end >= text_len:
                chunk = text[start:].strip()
                if chunk:
                    chunks.append(chunk)
                break

            # Try to break at a sentence or paragraph boundary
            chunk = text[start:end]
            last_newline = chunk.rfind('\n\n')
            if last_newline > chunk_size // 2:
                end = start + last_newline + 2
                chunk = text[start:end].strip()
            else:
                last_sentence = max(
                    chunk.rfind('. '),
                    chunk.rfind('!\n'),
                    chunk.rfind('?\n'),
                )
                if last_sentence > chunk_size // 2:
                    end = start + last_sentence + 1
                    chunk = text[start:end].strip()
                else:
                    chunk = chunk.strip()

            if chunk:
                chunks.append(chunk)

            start = end - overlap

        return chunks

    def get_context_for_query(self, session_id: str, query: str, max_chars: int = 6000) -> str:
        """Get relevant context from documents for a query."""
        chunks = self.search(session_id, query, n_results=5)
        if not chunks:
            return ""

        context_parts = []
        total = 0
        for chunk in chunks:
            header = f"\n[Source: {chunk['metadata'].get('filename', 'document')}]\n"
            text = header + chunk['content']
            if total + len(text) > max_chars:
                remaining = max_chars - total
                if remaining > 100:
                    context_parts.append(text[:remaining])
                break
            context_parts.append(text)
            total += len(text)

        return "\n---\n".join(context_parts)
