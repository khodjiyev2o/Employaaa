from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import database
from routers import authentication, users, companies, quizzes

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
app.include_router(authentication.router)
app.include_router(companies.router)
app.include_router(quizzes.router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def health_check():
    return {"status": "working from ci/cd"}
