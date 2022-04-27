from fastapi import FastAPI, Form, File
from fastapi.middleware.cors import CORSMiddleware

import json

import imagepy
from imagepy.app import ImageWeb

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


imweb = ImageWeb(None)
menus = imweb.load_menu_for_json()

def flatten(plgs, lst=None):
    if lst is None: lst = []
    if isinstance(plgs, tuple):
        if callable(plgs[1]): lst.append((plgs))
        else: flatten(plgs[1], lst)
    if isinstance(plgs, list):
        for i in plgs:
            if i == '-': 
                plgs.remove(i)
            else: 
                flatten(i, lst)
    return plgs

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/menu/')
def menu():
    # menu = json.dumps(flatten(menus)[1], default=lambda obj: obj.__dict__)
    menu = flatten(menus)[1]

    return menu

@app.get('/plugins/')
def plugins(id):
    exe = imweb.plugin_manager.get(id)
    print(exe)
    return "hello world"


@app.post('/img/')
async def img(file: str = Form(...)):
    print(file)
    return "hello, img"