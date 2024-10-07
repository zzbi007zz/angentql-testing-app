from typing import List
from backend.app.models.ai_model.model import AIModel
from datetime import datetime

# Placeholder for MongoDB integration
ai_models = []

async def create_ai_model(ai_model: AIModel) -> AIModel:
    ai_model.id = str(len(ai_models) + 1)
    ai_model.created_at = datetime.now().isoformat()
    ai_model.updated_at = datetime.now().isoformat()
    ai_models.append(ai_model)
    return ai_model

async def get_ai_models() -> List[AIModel]:
    return ai_models

async def update_ai_model(id: str, ai_model: AIModel) -> AIModel:
    for i, model in enumerate(ai_models):
        if model.id == id:
            ai_model.id = id
            ai_model.updated_at = datetime.now().isoformat()
            ai_models[i] = ai_model
            return ai_model
    return AIModel()

async def delete_ai_model(id: str) -> AIModel:
    for i, model in enumerate(ai_models):
        if model.id == id:
            deleted_model = ai_models.pop(i)
            return deleted_model
    return AIModel()