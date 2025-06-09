from datetime import datetime
from typing import Optional

class Stand:
    def __init__(self, stand_type: str, number: int):
        self.type = stand_type  # 'e' или 'a'
        self.number = number
        self.user: Optional[str] = None
        self.task: Optional[str] = None
        self.occupied_at: Optional[datetime] = None

    def is_occupied(self) -> bool:
        return self.user is not None

    def occupy(self, user: str, task: str):
        self.user = user
        self.task = task
        self.occupied_at = datetime.now()

    def free(self):
        self.user = None
        self.task = None
        self.occupied_at = None