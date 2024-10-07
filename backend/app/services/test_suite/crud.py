from typing import List
from backend.app.models.test_suite import TestSuite
from datetime import datetime

# Placeholder for MongoDB integration
test_suites = []

async def create_test_suite(test_suite: TestSuite) -> TestSuite:
    test_suite.id = str(len(test_suites) + 1)
    test_suite.created_at = datetime.now().isoformat()
    test_suite.updated_at = datetime.now().isoformat()
    test_suites.append(test_suite)
    return test_suite

async def get_test_suites() -> List[TestSuite]:
    return test_suites

async def update_test_suite(id: str, test_suite: TestSuite) -> TestSuite:
    for i, suite in enumerate(test_suites):
        if suite.id == id:
            test_suite.id = id
            test_suite.updated_at = datetime.now().isoformat()
            test_suites[i] = test_suite
            return test_suite
    return TestSuite()

async def delete_test_suite(id: str) -> TestSuite:
    for i, suite in enumerate(test_suites):
        if suite.id == id:
            deleted_suite = test_suites.pop(i)
            return deleted_suite
    return TestSuite()