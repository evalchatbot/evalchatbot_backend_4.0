"""
Short-term memory using a sliding window (collections.deque).
Organizes context by (user_id, session_id).
"""
from collections import deque
from typing import Deque, Dict, List, Tuple

class ShortTermMemory:
    """
    Manages short-term conversational memory as a fixed-size FIFO buffer.
    Each (user_id, session_id) gets its own deque with maxlen=window_size.
    """
    def __init__(self, window_size: int = 10):
        self.store: Dict[Tuple[str, str], Deque[dict]] = {}
        self.window_size = window_size

    def get_store(self, user_id: str, session_id: str) -> Deque[dict]:
        key = (user_id, session_id)
        if key not in self.store:
            self.store[key] = deque(maxlen=self.window_size)
        return self.store[key]

    def add_message(self, user_id: str, session_id: str, message: dict) -> None:
        self.get_store(user_id, session_id).append(message)

    def get_recent_messages(self, user_id: str, session_id: str) -> List[dict]:
        return list(self.get_store(user_id, session_id))

    def clear(self, user_id: str, session_id: str) -> None:
        key = (user_id, session_id)
        if key in self.store:
            del self.store[key]
