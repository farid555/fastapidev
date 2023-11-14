from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
# pydantic Create class Model [https://docs.pydantic.dev/latest/concepts/models/]


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your post"}


@app.post("/createposts")
def create_post(new_post: Post):
    print(dict(new_post))
    print(new_post.model_dump(mode='json'))
    return {"data": "new_post"}
