import os
import uvicorn

from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from routes.todos import router as todo_router

app = FastAPI(title="Todo API Service")

# add app routers
app.include_router(todo_router, tags=["todos"])


@app.on_event("startup")
async def startup():
    print("Todo Service is starting...")
    app.mongodb_client = MongoClient(str(os.environ.get("ATLAS_URI")))
    app.database = app.mongodb_client[str(os.environ.get("DB_NAME"))]
    try:
        app.database.command('ping')
        print("Connected to the MongoDB Database!")
        print("Todo Service is running...")
    except ConnectionFailure:
        print("MongoDB server not available.")


@app.on_event("shutdown")
async def shutdown():
    print("Todo Service is shutting down...")


def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("POST", "8000")), reload=True)
