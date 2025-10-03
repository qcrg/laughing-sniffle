from fastapi import FastAPI, APIRouter
from api import v0

app = FastAPI()

v0_router = APIRouter()
v0.init(v0_router)

app.include_router(v0_router, prefix="/v0")
