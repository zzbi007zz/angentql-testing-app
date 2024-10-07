from pydantic import BaseModel, Field
from typing import Optional, Dict

class TestExecutionResult(BaseModel):
    id: Optional[str] = Field(default=None)
    test_suite_id: str
    model_id: str
    query: str
    status: str
    response: Optional[Dict] = None
    error_message: Optional[str] = None
    created_at: Optional[str] = None