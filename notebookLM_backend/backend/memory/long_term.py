"""
Long-term memory management using Supabase.
Persists important facts, context, and user preferences.
"""
from typing import List, Dict, Any, Optional
from loguru import logger
from backend.db.supabase_client import SupabaseDB

class LongTermMemory:
    """
    Manages long-term memory by persisting key facts and context in Supabase.
    Organizes memory by user/session/context.
    """
    def __init__(self, table: str = "long_term_memory"):
        self.db = SupabaseDB()
        self.table = table  # Ensure this table exists with columns: user_id, session_id, context, fact

    def save_fact(self, user_id: str, session_id: str, context: str, fact: str) -> None:
        """Persist a fact or context snippet to Supabase."""
        try:
            payload = {
                "user_id": user_id,
                "session_id": session_id,
                "context": context,
                "fact": fact,
            }
            self.db.insert(self.table, payload)
        except Exception as e:
            logger.error(f"[LongTermMemory.save_fact] insert failed: {e}")

    def get_facts(
        self,
        user_id: str,
        session_id: Optional[str] = None,
        context: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieve facts for a user, optionally filtered by session/context."""
        try:
            filters = {"user_id": user_id}
            if session_id:
                filters["session_id"] = session_id
            if context:
                filters["context"] = context
            res = self.db.select(self.table, filters)
            return res.data if hasattr(res, "data") and res.data else []
        except Exception as e:
            logger.error(f"[LongTermMemory.get_facts] select failed: {e}")
            return []

    def clear(self, user_id: str, session_id: Optional[str] = None) -> None:
        """Delete facts for a user (optionally restricted to a session)."""
        try:
            filters = {"user_id": user_id}
            if session_id:
                filters["session_id"] = session_id
            self.db.delete(self.table, filters)
        except Exception as e:
            logger.error(f"[LongTermMemory.clear] delete failed: {e}")
