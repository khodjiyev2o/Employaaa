from email.policy import default
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from users.database import database
from routers import users
app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)

app.include_router(users.router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def HealthCheck():
    return {"status": "working"}

