import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel
# pydantic Create class Model [https://docs.pydantic.dev/latest/concepts/models/]
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from sqlalchemy.orm import Session
from .database import  engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency





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






@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


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
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {'post': post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s , content= %s, published= %s WHERE id = %s  RETURNING *""",
                   (post.title, post.content, post.published, (str(id))))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return {"message": updated_post}
