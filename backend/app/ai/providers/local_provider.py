import json
import logging
import httpx
from typing import List, Dict, Any
from app.ai.providers.base import BaseAIProvider
from app.schemas.ai import LLMMessage, LLMResponse

logger = logging.getLogger(__name__)

class LocalProvider(BaseAIProvider):
    def __init__(self, model_name: str = "llama3", base_url: str = "http://localhost:11434", **kwargs):
        super().__init__(model_name=model_name, **kwargs)
        self.base_url = base_url.rstrip("/")

    async def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.5,
        max_tokens: int = 2048,
        **kwargs
    ) -> LLMResponse:
        endpoint = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model_name,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(endpoint, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    content = data.get("message", {}).get("content", "")
                    return LLMResponse(content=content, provider="local", model=self.model_name)
        except Exception as e:
            logger.warning(f"Local provider connection to {endpoint} failed: {e}. Using deterministic local diplomat fallback.")
        
        # Fallback response
        return LLMResponse(
            content="[LOCAL ENGINE]: Simulated diplomatic response based on standard UNSC behavioral constraints.",
            provider="local_fallback",
            model=self.model_name
        )

    async def structured_generate(
        self,
        messages: List[LLMMessage],
        schema: Any,
        temperature: float = 0.2,
        **kwargs
    ) -> Any:
        sys_prompt = f"\nYou must output strictly valid JSON matching this schema: {schema.model_json_schema()}.\nDo not include any Markdown wrap or explanation outside the JSON."
        augmented_messages = list(messages)
        augmented_messages[0] = LLMMessage(
            role=augmented_messages[0].role,
            content=augmented_messages[0].content + sys_prompt
        )
        res = await self.generate(augmented_messages, temperature=temperature)
        try:
            clean_text = res.content.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            data = json.loads(clean_text.strip())
            return schema.model_validate(data)
        except Exception as e:
            logger.warning(f"Failed to parse structured JSON from local model: {e}")
            return None
