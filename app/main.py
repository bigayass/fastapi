
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from . import models
from .database import engine
from .routers import post, user, auth, vote
from . import schemas
import boto3
from fastapi.responses import JSONResponse, FileResponse
from os import getcwd
from .utils import create_new_name, upload_file


# Create all tables from our models
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {'message': "Social Media API"}

@app.post("/files/")
def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


# @app.post("/uploadfile/")
# def create_upload_file(author: str = Form(...), size: str = Form(...), file: UploadFile = File(...)):
    
#     return {"filename": file.filename, 'properties': schemas.FileData(size=size,author=author)}

@app.post("/uploadfile/")
async def create_upload_file(author: str = Form(...), size: str = Form(...), file: UploadFile = File(...)):

    # Create the new name
    new_name = create_new_name(file.filename)

    # save the file in media/image folder
    with open(f'media/images/{new_name}', 'wb') as image:
        content = await file.read()
        image.write(content)
        image.close()

    path = upload_file(new_name)

    return {"filename": file.filename, 'properties': schemas.FileData(size=size,author=author,path=path)}

# @app.post("/uploadfile/")
# async def create_upload_file(author: str = Form(...), size: str = Form(...), file: UploadFile = File(...)):

#     # Create the new name
#     new_name = create_new_name(file.filename)

#     # save the file in media/image folder
#     with open(f'media/images/{new_name}', 'wb') as image:
#         content = await file.read()
#         image.write(content)
#         image.close()

#     path = upload_file(new_name)

#     return {"filename": file.filename, 'properties': schemas.FileData(size=size,author=author,path=path)}



# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     with open(f'media/images/{file.filename}', 'wb') as image:
#         content = await file.read()
#         image.write(content)
#         image.close()
#     return JSONResponse(content={"filename": file.filename}, status_code=200)



@app.get("/download/{name_file}")
def download_file(name_file: str):
    return FileResponse(path=getcwd() + "/media/images/" + name_file, media_type='application/octet-stream', filename=name_file)




def my_schema():
   openapi_schema = get_openapi(
       title="Social Media API",
       version="1.0",
       description="Social media API that users can create accounts, login, and Create, Update and Delete posts",
       routes=app.routes,
   )
   app.openapi_schema = openapi_schema
   return app.openapi_schema

my_schema()





############################################## CRUD WITH SQL QUERYS ###############################################
'''
# connection to our database

#from fastapi.params import Body
#import psycopg2 #pip install psycopg2
#from psycopg2.extras import RealDictCursor

while True:
    try:
        conn = psycopg2.connect( 
            host='localhost',
            database='fastapi',
            user='postgres', 
            password='tigerbiga.26',
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        print("FastApi Database connection was succesful !") 
        break

    except Exception as error:
        print("Connection to Database failed")
        print("Error: ", error)
        time.sleep(2)

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {'data': posts}


@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    print(post)
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit()

    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int): # def get_post(id: int,response: Response)
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"Post with id: {id} was not found"}
    return {"post_detail": post}



@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    return {"date": post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
'''




