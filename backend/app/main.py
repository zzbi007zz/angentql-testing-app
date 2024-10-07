from fastapi import FastAPI
from .api.auth import router as auth_router
from .api.test_suites.routes import router as test_suite_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(test_suite_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)