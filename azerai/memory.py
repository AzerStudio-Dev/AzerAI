"""
AzerAI Memory - Danışıq Tarixçəsini İdarə Edir
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

class MemoryManager:
    def __init__(self, memory_file: str = "azerai_history.json"):
        self.memory_file = memory_file
        self.max_conversations = None  # Limitsiz danışıq sayı
        self.max_age_days = 7  # Danışıqların maksimum saxlanma müddəti (gün)
        self._ensure_memory_file()

    def _ensure_memory_file(self):
        """Yaddaş faylının varlığını yoxla və yoxsa yarat"""
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _load_conversations(self) -> List[Dict[str, Any]]:
        """Danışıqları fayldan yüklə"""
        try:
            if not os.path.exists(self.memory_file):
                return []
            
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                conversations = json.load(f)
                return conversations if isinstance(conversations, list) else []
        except Exception as e:
            print(f"Danışıqlar yüklənə bilmədi: {e}")
            return []

    def _save_conversations(self, conversations: List[Dict[str, Any]]):
        """Danışıqları fayla saxla"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Danışıqlar saxlana bilmədi: {e}")

    def _cleanup_old_conversations(self, conversations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Köhnə danışıqları təmizlə"""
        cutoff_date = datetime.now() - timedelta(days=self.max_age_days)
        filtered_conversations = []
        
        for conv in conversations:
            try:
                conv_date = datetime.fromisoformat(conv.get('timestamp', ''))
                if conv_date > cutoff_date:
                    filtered_conversations.append(conv)
            except:
                continue
        
        # Maksimum danışıq sayını qoru (əgər limitsizdirse)
        if self.max_conversations is not None:
            return filtered_conversations[-self.max_conversations:]
        else:
            return filtered_conversations

    def add_conversation(self, user_message: str, assistant_message: str):
        """Yeni danışıq əlavə et"""
        conversations = self._load_conversations()
        
        new_conversation = {
            'user_message': user_message,
            'assistant_message': assistant_message,
            'timestamp': datetime.now().isoformat()
        }
        
        conversations.append(new_conversation)
        conversations = self._cleanup_old_conversations(conversations)
        self._save_conversations(conversations)

    def get_memory_context(self) -> str:
        """Yaddaş kontekstini qaytar"""
        conversations = self._load_conversations()
        
        if not conversations:
            return ""
        
        # Bütün danışıqları al (limitsiz)
        recent_conversations = conversations
        
        context_parts = ["Əvvəlki danışıqlardan yadda saxla:"]
        for i, conv in enumerate(recent_conversations, 1):
            context_parts.append(f"{i}. İstifadəçi: {conv['user_message']}")
            context_parts.append(f"   Asistan: {conv['assistant_message']}")
        
        return "\n".join(context_parts) + "\n"

    def clear_memory(self):
        """Yaddaşı təmizlə"""
        self._save_conversations([])

    def get_conversation_count(self) -> int:
        """Danışıq sayısını qaytar"""
        conversations = self._load_conversations()
        return len(conversations)
