from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import imagepy
from imagepy.app import ImageWeb

import base64
import json
import shutil
from io import BytesIO
from PIL import Image, ImageFilter
import numpy as np
import cv2


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
    return "hello world"


# refs:
# https://levelup.gitconnected.com/how-to-save-uploaded-files-in-fastapi-90786851f1d3
# https://cloudbytes.dev/snippets/received-return-a-file-from-in-memory-buffer-using-fastapi
# https://stackoverflow.com/questions/71595635/render-numpy-array-in-fastapi
# https://stackoverflow.com/questions/71313129/how-to-render-streamable-image-on-react-coming-from-the-fastapi/71324775#71324775

# https://stackoverflow.com/questions/61333907/receiving-an-image-with-fast-api-processing-it-with-cv2-then-returning-it

# https://stackoverflow.com/questions/6375942/how-do-you-base-64-encode-a-png-image-for-use-in-a-data-uri-in-a-css-file

@app.post('/img/')
async def img(file: UploadFile = File(...), plugin: str = Form(...)):
    exe = imweb.plugin_manager.get(plugin)
    print('exe = ', exe().tag)

    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)

    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # img_dimensions = str(img.shape)

    # return_img = processImage(img)
    # return_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # return_img = img

    _, encoded_img = cv2.imencode('.PNG', return_img)

    encoded_img = base64.b64encode(encoded_img).decode('ascii')

    return {
        'filename': file.filename,
        'dimensions': {
            'height': img.shape[0],
            'width': img.shape[1],
            'channels': img.shape[2]
        },
        'encoded_img': 'data:image/png;base64,{}'.format(encoded_img),
    }
