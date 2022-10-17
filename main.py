from email.policy import default
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from users.database import db
from routers import authentication, users
app = FastAPI()


origins = [
    "http://localhost:8080",
]


app.include_router(authentication.router)
app.include_router(users.router)



@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
async def HealthCheck():
    return {"status": "working"}



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)