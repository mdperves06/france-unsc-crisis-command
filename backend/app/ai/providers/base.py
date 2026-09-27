from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.schemas.ai import LLMMessage, LLMResponse

class BaseAIProvider(ABC):
    """Abstract interface for all AI Providers (Local, Gemini, Claude, OpenAI)."""
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.kwargs = kwargs

    @abstractmethod
    async def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.5,
        max_tokens: int = 2048,
        **kwargs
    ) -> LLMResponse:
        """Generate text completion from messages."""
        pass

    @abstractmethod
    async def structured_generate(
        self,
        messages: List[LLMMessage],
        schema: Any,
        temperature: float = 0.3,
        **kwargs
    ) -> Any:
        """Generate structured response matching a Pydantic schema."""
        pass
