import json
import logging
import httpx
from typing import List, Dict, Any
from app.ai.providers.base import BaseAIProvider
from app.schemas.ai import LLMMessage, LLMResponse

logger = logging.getLogger(__name__)

class OpenAIProvider(BaseAIProvider):
    def __init__(self, model_name: str = "gpt-4o", api_key: str = "", base_url: str = "https://api.openai.com/v1", **kwargs):
        super().__init__(model_name=model_name, **kwargs)
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    async def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.5,
        max_tokens: int = 2048,
        **kwargs
    ) -> LLMResponse:
        if not self.api_key:
            return LLMResponse(
                content="[SIMULATION ENGINE - OPENAI KEY NOT SET]: Offline diplomatic fallback response.",
                provider="openai_sim",
                model=self.model_name
            )
        endpoint = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model_name,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                res = await client.post(endpoint, json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    content = data["choices"][0]["message"]["content"]
                    return LLMResponse(content=content, provider="openai", model=self.model_name)
        except Exception as e:
            logger.warning(f"OpenAI request error: {e}")

        return LLMResponse(content="[OFFLINE SIMULATION]: Fallback response.", provider="openai_fallback", model=self.model_name)

    async def structured_generate(
        self,
        messages: List[LLMMessage],
        schema: Any,
        temperature: float = 0.2,
        **kwargs
    ) -> Any:
        sys_prompt = f"\nReturn strictly valid JSON adhering to schema:\n{schema.model_json_schema()}"
        augmented = list(messages)
        augmented[-1] = LLMMessage(role=augmented[-1].role, content=augmented[-1].content + sys_prompt)
        res = await self.generate(augmented, temperature=temperature)
        try:
            clean = res.content.strip()
            if clean.startswith("```json"): clean = clean[7:]
            if clean.startswith("```"): clean = clean[3:]
            if clean.endswith("```"): clean = clean[:-3]
            return schema.model_validate_json(clean.strip())
        except Exception as e:
            logger.warning(f"OpenAI structured parsing failed: {e}")
            return None
