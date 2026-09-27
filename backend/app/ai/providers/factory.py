from app.core.config import settings
from app.ai.providers.base import BaseAIProvider
from app.ai.providers.local_provider import LocalProvider
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.providers.claude_provider import ClaudeProvider
from app.ai.providers.openai_provider import OpenAIProvider

def get_provider_for_agent(agent_type: str) -> BaseAIProvider:
    """
    Factory to retrieve configured AI Provider for each of the 4 specialist agents:
    - 'research'
    - 'country'
    - 'coach'
    - 'orchestrator'
    """
    provider_type = "local"
    model_name = "llama3"

    if agent_type == "research":
        provider_type = settings.AGENT_RESEARCH_PROVIDER
        model_name = settings.AGENT_RESEARCH_MODEL
    elif agent_type == "country":
        provider_type = settings.AGENT_COUNTRY_PROVIDER
        model_name = settings.AGENT_COUNTRY_MODEL
    elif agent_type == "coach":
        provider_type = settings.AGENT_COACH_PROVIDER
        model_name = settings.AGENT_COACH_MODEL
    elif agent_type == "orchestrator":
        provider_type = settings.AGENT_ORCHESTRATOR_PROVIDER
        model_name = settings.AGENT_ORCHESTRATOR_MODEL

    # Enforce global AI_MODE override if set to LOCAL ONLY or CLOUD ONLY
    if settings.AI_MODE == "LOCAL":
        provider_type = "local"

    provider_type = provider_type.lower()

    if provider_type == "gemini":
        return GeminiProvider(model_name=model_name, api_key=settings.GEMINI_API_KEY or "")
    elif provider_type == "claude":
        return ClaudeProvider(model_name=model_name, api_key=settings.ANTHROPIC_API_KEY or "")
    elif provider_type == "openai":
        return OpenAIProvider(model_name=model_name, api_key=settings.OPENAI_API_KEY or "")
    else:
        return LocalProvider(model_name=model_name, base_url=settings.LOCAL_AI_BASE_URL)
