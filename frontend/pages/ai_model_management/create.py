import streamlit as st
from backend.app.models.ai_model.model import AIModel
from backend.app.services.ai_model.crud import create_ai_model

def ai_model_create_page():
    st.title("Create AI Model")

    model_id = st.text_input("Model ID")
    name = st.text_input("Name")
    description = st.text_area("Description")
    api_key = st.text_input("API Key")

    if st.button("Create"):
        ai_model = AIModel(
            model_id=model_id,
            name=name,
            description=description,
            api_key=api_key,
            created_by="current_user.username"
        )
        created_model = create_ai_model(ai_model)
        st.success(f"AI Model '{created_model.name}' created successfully!")