import streamlit as st
from backend.app.services.test_suite.crud import get_test_suites
from frontend.components.test_suite_list.component import test_suite_list_component

def test_suite_view_page():
    st.title("Test Suite Management")

    test_suites = get_test_suites()
    test_suite_list_component(test_suites)