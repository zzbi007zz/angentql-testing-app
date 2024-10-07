from pydantic import BaseModel, Field
from typing import Optional

class AIModel(BaseModel):
    id: Optional[str] = Field(default=None)
    model_id: str
    name: str
    description: str
    api_key: str
    created_by: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None