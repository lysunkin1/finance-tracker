from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, categories, stats, tags, transactions, users

app = FastAPI(
    title="Finance Tracker API",
    description="REST API for tracking personal income and expenses",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(tags.router)
app.include_router(transactions.router)
app.include_router(stats.router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "Finance Tracker API is running"}
