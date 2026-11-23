from fastapi import FastAPI

app = FastAPI(title="Forja0.1")

from user_router import user_router

app.include_router(user_router)