"""
Short-term memory management using LangGraph's InMemoryStore.
Organizes context by (user_id, session_id).
"""
from typing import List, Dict, Tuple
from langgraph.store.memory import InMemoryStore

class ShortTermMemory:
    """
    Manages short-term conversational memory using LangGraph's InMemoryStore.
    Organizes memory by (user_id, session_id).
    """
    def __init__(self, window_size: int = 10):
        self.store: Dict[Tuple[str, str], InMemoryStore] = {}
        self.window_size = window_size

    def get_store(self, user_id: str, session_id: str) -> InMemoryStore:
        key = (user_id, session_id)
        if key not in self.store:
            self.store[key] = InMemoryStore(maxlen=self.window_size)
        return self.store[key]

    def add_message(self, user_id: str, session_id: str, message: dict) -> None:
        store = self.get_store(user_id, session_id)
        store.append(message)

    def get_recent_messages(self, user_id: str, session_id: str) -> List[dict]:
        store = self.get_store(user_id, session_id)
        return list(store)

    def clear(self, user_id: str, session_id: str) -> None:
        key = (user_id, session_id)
        if key in self.store:
            del self.store[key]
