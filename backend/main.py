from typing import Union
from fastapi.middleware.cors  import CORSMiddleware
from fastapi import FastAPI
from userRoutes.user import router as user_router
from database.database import SessionLocal,engine
from schema import schema
from getdb import get_db

app = FastAPI()
app.include_router(user_router)

schema.Base.metadata.create_all(bind=engine)
origins=['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}