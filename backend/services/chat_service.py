import uuid
from typing import Optional


class ChatService:
    """Service for chat operations"""

    # Keyword-based responses for demo purposes
    KEYWORD_RESPONSES = {
        "gdzie": "Mogę Ci pomóc zaplanować podróż! Gdzie chciałbyś pojechać?",
        "pogoda": "Aby sprawdzić pogodę w konkretnym miejscu, powiedz mi gdzie Cię interesuje.",
        "hotel": "Chętnie pomogę Ci znaleźć hotel. Powiedz mi jakie są Twoje preferencje i budżet.",
        "loty": "Mogę Ci pomóc znaleźć loty. Powiedz mi skąd i dokąd chcesz lecieć oraz kiedy.",
        "atrakcje": "Jakie atrakcje Cię interesują? Mogę zasugerować wiele fajnych miejsc.",
    }

    @staticmethod
    def get_chat_response(message: str) -> dict:
        """Get chat response based on message content"""
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")

        message_lower = message.lower()

        # Simple keyword matching for demo purposes
        response_content = next(
            (v for k, v in ChatService.KEYWORD_RESPONSES.items() if k in message_lower),
            f'Interesująca wiadomość! Rozumiem, że mówisz o: "{message}". Mogę Ci pomóc w planowaniu podróży.',
        )

        return {
            "id": str(uuid.uuid4()),
            "content": response_content,
        }
