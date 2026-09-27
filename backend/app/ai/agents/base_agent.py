from abc import ABC
from app.ai.providers.factory import get_provider_for_agent
from app.ai.providers.base import BaseAIProvider

class BaseAgent(ABC):
    def __init__(self, agent_name: str, agent_type: str):
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.provider: BaseAIProvider = get_provider_for_agent(agent_type)
