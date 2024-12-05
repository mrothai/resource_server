from fastapi import FastAPI, Header, Query , UploadFile, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import requests
#import fruitmodel
#pip install uvicorn
#uvicorn server.main:app
#pip install python-multipart
from models.fruit_model import FruitModel

#get

app = FastAPI()

#fruits = ["Apple","banana","Orange","mango","Bluebery","Strawberry","Pineapple","Watermelon","Grapes"]

fruits =[
    FruitModel(name="Apple",price=20),
    FruitModel(name="Orange",price=40),
    FruitModel(name="Grapes",price=60),
]

@app.get("/fruits")
def get_fruits():
    return fruits

# ดูผลไม้ตำแหน่ง N
@app.get("/fruits/{n}")
def get_fruit_by_number(n:int):
    if 0 <= n < len(fruits):
        return fruits[n]
    return {"error": "Index out of range"}


@app.get("/search-fruits")
def get_fruit_by_name(search:str = Query('')):
    result = []
    for fruit in fruits:
        if search.lower() in fruit.lower():
            result.append(fruit)

    return result

@app.post("/fruits")
def add_fruit(fruit:FruitModel  ,  token: str=Header(None)):
    if token is None:
        raise HTTPException(status_code=401,detail="Token is missing")
    #identify token
    user_id = identify(token)
    if user_id in ["123","321"]:
        if fruit.price is None:
            return "Price is not provide"
        fruits.append(fruit)
        return {"status": "success"}
    else:
        raise HTTPException(status_code=401,detail="unauthorized") 

@app.delete("/fruits")
def delete_fruit(fruit:FruitModel  ,  token: str=Header(None)):
     if token is None:
        raise HTTPException(status_code=401,detail="Token is missing")
    #identify token
        user_id = identify(token)
        if user_id in ["123","321"]:
            for f in fruits:
                if f.name.lower() == fruit.name.lower():
                    fruits.remove(f)
            return "success"
        else:
            raise HTTPException(status_code=401,detail="unauthorized") 

@app.put("/fruits")
def update_fruit(fruit:FruitModel  ,  token: str=Header(None)):
    if token is None:
        raise HTTPException(status_code=401,detail="Token is missing")
    #identify token
        user_id = identify(token)
        if user_id in ["123","321"]:
            if fruit.price == None:
                return "price is not proviced"
            for f in fruits:
                if f.name.lower() == fruit.name.lower():
                    f.price = fruit.price
            return "success"
        else:
            raise HTTPException(status_code=401,detail="unauthorized") 
    

@app.post("/file")
def upload_file(file:UploadFile):
    try:
        with open(f"server/files/{file.filename}","wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
        return f"file uploaded as: {file.filename}"
    except:
        raise HTTPException(status_code=400,detail="File uploaded failed")
    

@app.get("/file/{filename}")
def download_file(filename:str):
    filepath = f"server/files/{filename}"
    if os.path.isfile(filepath):
        return FileResponse(filepath, filename=filename)
    else:
        raise HTTPException(status_code=404,detail="File not found")

#ใช้ตรวจเช็ค token กับ auth_server
def identify(token: str):
   response = requests.post("http://127.0.0.1:8000/identify",
                  json={
                      "token": token,
                  },)
   
   if response.status_code == 200:
       return response.json()
   else:
       return None