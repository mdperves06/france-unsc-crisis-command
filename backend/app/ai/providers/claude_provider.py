import json
import logging
import httpx
from typing import List, Dict, Any
from app.ai.providers.base import BaseAIProvider
from app.schemas.ai import LLMMessage, LLMResponse

logger = logging.getLogger(__name__)

class ClaudeProvider(BaseAIProvider):
    def __init__(self, model_name: str = "claude-opus-5", api_key: str = "", **kwargs):
        super().__init__(model_name=model_name, **kwargs)
        self.api_key = api_key

    async def generate(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.5,
        max_tokens: int = 2048,
        **kwargs
    ) -> LLMResponse:
        if not self.api_key:
            return LLMResponse(
                content="[SIMULATION ENGINE - ANTHROPIC KEY NOT SET]: Offline strategic coach response.",
                provider="claude_sim",
                model=self.model_name
            )
        endpoint = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        system_msg = ""
        user_messages = []
        for m in messages:
            if m.role == "system":
                system_msg += m.content + "\n"
            else:
                user_messages.append({"role": m.role, "content": m.content})

        payload = {
            "model": self.model_name,
            "system": system_msg.strip(),
            "messages": user_messages,
            # Current Claude models reject sampling params (temperature/top_p) with a 400
            "max_tokens": max_tokens,
        }

        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                res = await client.post(endpoint, json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    # Response may start with a thinking block; keep only text blocks
                    content = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
                    return LLMResponse(content=content, provider="claude", model=self.model_name)
                logger.warning(f"Claude API returned status {res.status_code}: {res.text}")
        except Exception as e:
            logger.warning(f"Claude request error: {e}")

        return LLMResponse(content="[OFFLINE COACH]: Strategic simulation response.", provider="claude_fallback", model=self.model_name)

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
            logger.warning(f"Claude structured parsing failed: {e}")
            return None
