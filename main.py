from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
# pydantic Create class Model [https://docs.pydantic.dev/latest/concepts/models/]
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "Hello there!", "content": "This my third time", "id": 1}, {
    "title": "Hello there", "content": "This my third time", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def finde_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    post_dict = dict(new_post)
    post_dict['id'] = randrange(0, 100)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id:{id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {'test': post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index = finde_index_post(id)
    my_posts.pop(index)
    return {'message': 'post was succesfully deleted'}
