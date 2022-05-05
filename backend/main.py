from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import json
import shutil
from io import BytesIO
from PIL import Image, ImageFilter

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


# refs:
# https://levelup.gitconnected.com/how-to-save-uploaded-files-in-fastapi-90786851f1d3
# https://cloudbytes.dev/snippets/received-return-a-file-from-in-memory-buffer-using-fastapi
# https://stackoverflow.com/questions/71595635/render-numpy-array-in-fastapi
# https://stackoverflow.com/questions/71313129/how-to-render-streamable-image-on-react-coming-from-the-fastapi/71324775#71324775

@app.post('/img/')
async def img(img: UploadFile):
    print("file = ", img.filename)
    # with open("destination.png", "wb") as buffer:
    #     shutil.copyfileobj(img.file, buffer)
    # return img.filename

    original_image = Image.open(img.file)
    original_image = original_image.filter(ImageFilter.BLUR)

    filtered_image = BytesIO()
    original_image.save(filtered_image, "PNG")
    filtered_image.seek(0)

    return StreamingResponse(filtered_image, media_type="image/png")
