from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Form
from typing import List
import uvicorn
from pydantic import BaseModel, Field

app = FastAPI()

class Student(BaseModel):
    id: int
    name: str = Field(None, title='The name of the student', max_length=10)
    subject: List[str] = []
class User(BaseModel):
    name: str
    password: str = Field(None, min_length=5, max_length=20)
template = Jinja2Templates(directory="template")
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
async def root(request: Request, name: str):
    return template.TemplateResponse("hello.html", {"request": request, "name": name})

@app.post("/student/{college}")
async def student_data(college:str, age:int, sl: Student):
    retravel = {"college": college,"age": age, **sl.dict()}
    return retravel 

@app.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
   return template.TemplateResponse("login.html", {"request": request})

@app.post("/submit/")
async def submit(nm:str = Form(...), pwd:str = Form(...)):
    return User(name=nm, password=pwd)


if __name__ == "__main__":
    uvicorn.run("main:app", host = '0.0.0.0', port = 8000, reload = True)