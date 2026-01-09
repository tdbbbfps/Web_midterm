from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from user.router import router as user_router
from item.router import router as item_router
from user.models import User
from item.models import Item
import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="FastAPI",
    description="This is the API.",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/user", tags=["user"])
app.include_router(item_router, prefix="/api/item", tags=["item"])

@app.get("/")
async def root():
    return {"message": "Hello World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    print()