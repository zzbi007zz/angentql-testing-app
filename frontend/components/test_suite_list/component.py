import streamlit as st
from backend.app.models.test_suite import TestSuite

def test_suite_list_component(test_suites: list[TestSuite]):
    st.subheader("Test Suites")
    for test_suite in test_suites:
        with st.expander(test_suite.name):
            st.write(test_suite.description)
            st.write(f"Status: {test_suite.status}")
            st.write(f"Created by: {test_suite.created_by}")
            st.write(f"Created at: {test_suite.created_at}")
            st.write(f"Updated at: {test_suite.updated_at}")