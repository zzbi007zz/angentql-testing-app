import asyncio
from typing import List
from backend.app.models.test_execution.result import TestExecutionResult
from backend.app.services.agentql.agentql_service import AgentQLService
from backend.app.utils.agentql.agentql_helper import get_agentql_api_key, handle_rate_limiting

class TestExecutor:
    def __init__(self):
        self.agentql_service = AgentQLService(get_agentql_api_key())

    async def execute_test_suite(self, test_suite_id: str) -> List[TestExecutionResult]:
        results = []
        # Fetch test cases for the given test suite
        test_cases = await self.fetch_test_cases(test_suite_id)
        for test_case in test_cases:
            result = await self.execute_test_case(test_case)
            results.append(result)
        return results

    async def execute_test_case(self, test_case: dict) -> TestExecutionResult:
        result = TestExecutionResult(
            test_suite_id=test_case["test_suite_id"],
            model_id=test_case["model_id"],
            query=test_case["query"],
            status="pending"
        )
        try:
            response = await self.agentql_service.execute_query(test_case["model_id"], test_case["query"])
            result.status = "success"
            result.response = response
        except Exception as e:
            result.status = "failed"
            result.error_message = str(e)
        return result

    async def fetch_test_cases(self, test_suite_id: str) -> List[dict]:
        # Fetch test cases from the database for the given test suite
        return []