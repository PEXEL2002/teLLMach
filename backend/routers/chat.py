from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import ChatRequest, ChatResponse
from core import get_db, get_current_user
from services import ChatService

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def chat(
    chat_request: ChatRequest,
    current_user = Depends(get_current_user),
) -> ChatResponse:
    """AI Travel Assistant chat endpoint - sends message and receives response"""
    try:
        response_data = ChatService.get_chat_response(chat_request.message.strip())
        return ChatResponse(**response_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
