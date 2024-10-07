import streamlit as st
from backend.app.utils.agentql.agentql_helper import get_agentql_api_key

def agentql_config_page():
    st.title("AgentQL Configuration")

    api_key = st.text_input("AgentQL API Key", value=get_agentql_api_key())

    if st.button("Save"):
        # Save the API key to the environment
        st.success("AgentQL API key saved successfully!")