from typing import Optional, List
from datetime import datetime, timedelta
from pathlib import Path
import json

from config.settings import AUTO_FREE_DAYS
from models.stand import Stand


class StandManager:
    def __init__(self):
        self.stands: List[Stand] = []
        self.load_initial_stands()

    def load_initial_stands(self):
        """Инициализация стендов"""
        from config.constants import NUM_STANDS_E, NUM_STANDS_A
        
        # Создаем основные стенды (e1-e8)
        for i in range(1, NUM_STANDS_E + 1):
            self.stands.append(Stand('e', i))
        
        # Создаем админские стенды (a1-a3)
        for i in range(1, NUM_STANDS_A + 1):
            self.stands.append(Stand('a', i))

    def get_stand(self, stand_type: str, number: int) -> Optional[Stand]:
        """Получить стенд по типу и номеру"""
        for stand in self.stands:
            if stand.type == stand_type.lower() and stand.number == number:
                return stand
        return None

    def check_and_free_expired(self) -> List[str]:
        """Освобождает стенды, которые заняты дольше AUTO_FREE_DAYS дней"""
        current_time = datetime.now()
        freed = []
        
        for stand in self.stands:
            if stand.is_occupied() and stand.occupied_at:
                if (current_time - stand.occupied_at) >= timedelta(days=AUTO_FREE_DAYS):
                    freed.append(f"{stand.type}{stand.number}")
                    stand.free()
        
        return freed
    
    def load_from_json(self, stands_data: list):
        """Загружает данные из JSON"""
        for i, stand_data in enumerate(stands_data):
            if i >= len(self.stands):
                break
            
            self.stands[i].user = stand_data.get('user')
            self.stands[i].task = stand_data.get('task')
        
            if stand_data.get('occupied_at'):
                self.stands[i].occupied_at = datetime.fromisoformat(stand_data['occupied_at'])
            else:
                self.stands[i].occupied_at = None

# Создаем экземпляр менеджера для использования в других модулях
stand_manager = StandManager()