from pydantic import BaseModel, Field
from typing import Optional

class AgentQLQuery(BaseModel):
    id: Optional[str] = Field(default=None)
    model_id: str
    query: str
    result: Optional[dict] = None
    created_by: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None