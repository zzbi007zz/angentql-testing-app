import streamlit as st
from backend.app.services.ai_model.crud import get_ai_models

def ai_model_list_page():
    st.title("AI Model Management")

    ai_models = get_ai_models()

    for ai_model in ai_models:
        with st.expander(ai_model.name):
            st.write(ai_model.description)
            st.write(f"Model ID: {ai_model.model_id}")
            st.write(f"API Key: {ai_model.api_key}")
            st.write(f"Created by: {ai_model.created_by}")
            st.write(f"Created at: {ai_model.created_at}")
            st.write(f"Updated at: {ai_model.updated_at}")