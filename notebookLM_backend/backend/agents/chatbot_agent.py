"""
Chatbot Agent module.
Handles RAG pipeline, vector search, and memory management (short-term and long-term).
"""
from typing import Dict, Any, List
from backend.memory.short_term import ShortTermMemory
from backend.memory.long_term import LongTermMemory
from backend.db.supabase_client import SupabaseDB
from backend.config import GROQ_API_KEY, CHATBOT_LLM_MODEL
from backend.rag.embedding import FastEmbedEmbedding
from backend.rag.context import create_context_from_chunks
import httpx

class ChatbotAgent:
    """
    Chatbot agent with RAG pipeline, vector search, and memory integration.
    """
    def __init__(self):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()
        self.db = SupabaseDB()
        self.llm_model = CHATBOT_LLM_MODEL
        self.groq_api_key = GROQ_API_KEY
        self.embedding = FastEmbedEmbedding()

    async def ask(
        self,
        user_id: str,
        session_id: str,
        question: str,
        genre: str,
        book_ids: List[str] = None
    ) -> Dict[str, Any]:
        """
        Process a user question with RAG, memory, and vector search (async).
        Returns answer, source snippets, and retrieval metadata.
        """
        # 1. Generate query embedding
        query_embedding = await self.embedding.generate(question)
        # 2. Get book_ids (if not provided, fetch by genre)
        if not book_ids:
            books_res = self.db.select("books", {"genre": genre})
            book_ids = [b["id"] for b in books_res.data] if hasattr(books_res, 'data') else []
        # 3. Retrieve relevant document chunks (async vector search)
        chunks = await self.db.search_chunks_vector(query_embedding, book_ids, top_k=5)
        # 4. Add book titles to chunks (optional, can be optimized)
        if chunks:
            unique_book_ids = list(set(chunk["book_id"] for chunk in chunks))
            books_data = self.db.select("books", {"id": unique_book_ids})
            book_map = {book["id"]: book for book in books_data.data} if hasattr(books_data, 'data') else {}
            for chunk in chunks:
                book = book_map.get(chunk["book_id"])
                if book:
                    chunk["book_title"] = book["title"]
                    chunk["book_author"] = book["author"]
        # 5. Create context from chunks
        context_str = create_context_from_chunks(chunks)
        # 6. Get recent chat context from short-term memory
        context = self.short_term.get_recent_messages(user_id, session_id)
        # 7. Compose prompt for LLM
        prompt = self._compose_prompt(question, context, context_str)
        # 8. Get answer from LLM (GROQ API)
        answer = self._call_llm_groq(prompt)
        # 9. Optionally persist important facts to long-term memory
        self.long_term.save_fact(user_id, session_id, context="chat", fact=answer)
        # 10. Add user/assistant messages to short-term memory
        self.short_term.add_message(user_id, session_id, {"sender": "user", "message": question})
        self.short_term.add_message(user_id, session_id, {"sender": "assistant", "message": answer})
        return {
            "answer": answer,
            "sources": chunks,
            "context": context,
            "metadata": {"retrieved_chunks": len(chunks)}
        }

    def _compose_prompt(self, question: str, chat_context: List[dict], context_str: str) -> str:
        """Compose prompt for LLM using chat history and retrieved chunks."""
        chat_history = "\n".join([m["message"] for m in chat_context])
        return f"System: You are a helpful book assistant.\nChat History:\n{chat_history}\n\nRelevant Book Context:\n{context_str}\n\nQuestion: {question}\nAnswer:"

    def _call_llm_groq(self, prompt: str) -> str:
        """Call the GROQ API to get an answer from the configured LLM model."""
        if not self.groq_api_key or not self.llm_model:
            return "[Error: GROQ API key or model not configured]"
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.llm_model,
            "messages": [
                {"role": "system", "content": "You are a helpful book assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 512,
            "temperature": 0.7
        }
        try:
            with httpx.Client(timeout=30) as client:
                response = client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[GROQ API error: {e}]"
