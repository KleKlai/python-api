from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = False # Default value False
    rating: Optional[int] = None

my_posts = [{"title":"title of post 1", "content": "content of post 1", "id": 1}, 
            {"title":"title of post 2", "content": "content of post 2", "id": 2}]

@app.get("/")
async def root():
    return {"message": "Hello Maynard Magallen etc"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(int(id))

    # if not post:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"message": f"post with id: {id} was not found"}

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    return {"data": post}

def find_index_post(id):

    # check if id exist

    for p in my_posts:
        if p["id"] == id:
            continue

    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    my_posts.pop(index)

    # You are sending 204 we should not send the data back
    return Response(status_code=status.HTTP_204_NO_CONTENT)