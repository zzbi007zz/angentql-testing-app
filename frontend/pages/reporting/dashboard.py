import streamlit as st
from backend.app.services.reporting.aggregator import ReportingAggregator

def reporting_dashboard_page():
    st.title("Reporting and Analytics")

    test_suite_id = st.text_input("Test Suite ID")

    aggregator = ReportingAggregator()
    success_rate = aggregator.get_test_suite_success_rate(test_suite_id)
    test_case_results = aggregator.get_test_case_results(test_suite_id)

    st.metric("Test Suite Success Rate", f"{success_rate * 100:.2f}%")

    st.subheader("Test Case Results")
    for result in test_case_results:
        with st.expander(result["query"]):
            st.write(f"Status: {result['status']}")
            if result['status'] == "failed":
                st.write(f"Error: {result['error_message']}")