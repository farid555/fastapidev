import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
# pydantic Create class Model [https://docs.pydantic.dev/latest/concepts/models/]
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='123456', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull...")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error", error)
        time.sleep(2)


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
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)  RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"message": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {'post': post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    index = finde_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    my_posts.pop(index)
    return Response(tatus_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = finde_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    post_dict = post.model_dump(mode='json')
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"message": post_dict}
