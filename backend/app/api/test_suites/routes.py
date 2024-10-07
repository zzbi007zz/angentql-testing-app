from fastapi import APIRouter, Depends
from backend.app.models.test_suite import TestSuite
from backend.app.models.user import User
from backend.app.services.test_suite.crud import create_test_suite, get_test_suites, update_test_suite, delete_test_suite
from backend.app.services.auth import AuthService

router = APIRouter()

@router.post("/", response_model=TestSuite)
async def create_new_test_suite(test_suite: TestSuite, current_user: User = Depends(AuthService.get_current_user)):
    return await create_test_suite(test_suite)

@router.get("/", response_model=list[TestSuite])
async def list_test_suites(current_user: User = Depends(AuthService.get_current_user)):
    return await get_test_suites()

@router.put("/{id}", response_model=TestSuite)
async def update_test_suite_by_id(id: str, test_suite: TestSuite, current_user: User = Depends(AuthService.get_current_user)):
    return await update_test_suite(id, test_suite)

@router.delete("/{id}", response_model=TestSuite)
async def delete_test_suite_by_id(id: str, current_user: User = Depends(AuthService.get_current_user)):
    return await delete_test_suite(id)