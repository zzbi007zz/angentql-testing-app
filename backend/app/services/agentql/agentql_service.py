from typing import Dict, Any
from agentql import AgentQL

class AgentQLService:
    def __init__(self, api_key: str):
        self.agentql = AgentQL(api_key)

    def execute_query(self, model_id: str, query: str) -> Dict[str, Any]:
        return self.agentql.execute(model_id, query)

    def list_models(self) -> Dict[str, Any]:
        return self.agentql.list_models()