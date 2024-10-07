import streamlit as st
from backend.app.models.test_suite import TestSuite
from backend.app.services.test_suite.crud import create_test_suite

def test_suite_create_page():
    st.title("Create Test Suite")

    name = st.text_input("Name")
    description = st.text_area("Description")

    if st.button("Create"):
        test_suite = TestSuite(
            name=name,
            description=description,
            created_by="current_user.username"
        )
        created_test_suite = create_test_suite(test_suite)
        st.success(f"Test suite '{created_test_suite.name}' created successfully!")