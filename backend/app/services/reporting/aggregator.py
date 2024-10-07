from typing import List, Dict
from backend.app.models.test_execution.result import TestExecutionResult
from pymongo import MongoClient

class ReportingAggregator:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.agentql_testing_app

    def get_test_suite_success_rate(self, test_suite_id: str) -> float:
        pipeline = [
            {"$match": {"test_suite_id": test_suite_id}},
            {"$group": {
                "_id": "$status",
                "count": {"$count": {}}
            }},
            {"$project": {
                "status": "$_id",
                "count": "$count",
                "_id": 0
            }}
        ]
        results = list(self.db.test_execution_results.aggregate(pipeline))
        total_count = sum(result["count"] for result in results)
        success_count = next((result["count"] for result in results if result["status"] == "success"), 0)
        return success_count / total_count if total_count > 0 else 0.0

    def get_test_case_results(self, test_suite_id: str) -> List[Dict]:
        pipeline = [
            {"$match": {"test_suite_id": test_suite_id}},
            {"$project": {
                "query": 1,
                "status": 1,
                "error_message": 1
            }}
        ]
        return list(self.db.test_execution_results.aggregate(pipeline))