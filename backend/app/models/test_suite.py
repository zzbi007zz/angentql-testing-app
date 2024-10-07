from pydantic import BaseModel, Field
from typing import Optional

class TestSuite(BaseModel):
    id: Optional[str] = Field(default=None)
    name: str
    description: str
    status: str = "draft"
    created_by: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None