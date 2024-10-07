import streamlit as st
from backend.app.services.agentql.agentql_service import AgentQLService
from backend.app.utils.agentql.agentql_helper import get_agentql_api_key
from backend.app.models.agentql_query import AgentQLQuery

def agentql_execute_page():
    st.title("Execute AgentQL Query")

    model_id = st.text_input("Model ID")
    query = st.text_area("Query")

    if st.button("Execute"):
        agentql_service = AgentQLService(get_agentql_api_key())
        result = agentql_service.execute_query(model_id, query)
        agentql_query = AgentQLQuery(
            model_id=model_id,
            query=query,
            result=result,
            created_by="current_user.username"
        )
        # Save the AgentQL query to the database
        st.json(result)