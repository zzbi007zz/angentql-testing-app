import streamlit as st
from backend.app.services.test_execution.executor import TestExecutor
from backend.app.models.test_execution.result import TestExecutionResult

def test_execution_page():
    st.title("Test Execution")

    test_suite_id = st.text_input("Test Suite ID")

    if st.button("Execute"):
        executor = TestExecutor()
        results = executor.execute_test_suite(test_suite_id)
        for result in results:
            with st.expander(f"Test Case: {result.query}"):
                st.write(f"Status: {result.status}")
                if result.status == "success":
                    st.json(result.response)
                else:
                    st.write(f"Error: {result.error_message}")