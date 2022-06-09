from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List
from pydantic import BaseModel

import imagepy
from imagepy.app import ImageWeb
from sciapp.object import Image, ROI
from sciapp.util.shputil import json2shp, geom2shp, xy_canvas2np

import base64
import json
import numpy as np
import cv2
from PIL import Image as PILImage
from io import BytesIO
import copy

import geojson

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


imweb = ImageWeb()
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
    if exe().view:
        print("view = ", exe().view)
        view = []
        for i in exe().view:
            if i[0] == list:
                view.append(('list', *i[1:3], i[3].__name__, *i[4:]))
            elif type(i[0]) == type:
                view.append((i[0].__name__, *i[1:]))
            else:
                view.append((i[0], *i[1:]))

        print("dialog = ", view)
        return view, exe().para
    else:
        return None


# refs:
# https://levelup.gitconnected.com/how-to-save-uploaded-files-in-fastapi-90786851f1d3
# https://cloudbytes.dev/snippets/received-return-a-file-from-in-memory-buffer-using-fastapi
# https://stackoverflow.com/questions/71595635/render-numpy-array-in-fastapi
# https://stackoverflow.com/questions/71313129/how-to-render-streamable-image-on-react-coming-from-the-fastapi/71324775#71324775

# https://stackoverflow.com/questions/61333907/receiving-an-image-with-fast-api-processing-it-with-cv2-then-returning-it

# https://stackoverflow.com/questions/6375942/how-do-you-base-64-encode-a-png-image-for-use-in-a-data-uri-in-a-css-file


@app.post('/img/')
async def img(
    file: UploadFile = File(...), 
    plugin: str = Form(...),
    para: str = Form(...),
    roi: str = Form(...) 
    ):

    # read file stream
    contents = await file.read()
    pil_img = PILImage.open(BytesIO(contents))
    img = np.asarray(pil_img)
    print("img after decoding = ", img.shape)

    # read roi
    old_roi = json.loads(roi)
    print("old_roi in json = ", old_roi)

    # create Image Object
    imgPlus = Image([img])
    if old_roi:
        print("*****************************************************")
        xy_canvas2np(old_roi, img.shape)
        # print("successful!!!")
        # print("old_roi in json 222 = ", old_roi)
        print("*****************************************************")

        imgPlus.roi = ROI(json2shp(old_roi))

    imweb.show_img(imgPlus, file.filename)

    exe = imweb.plugin_manager.get(plugin)
    try:
        para = json.loads(para)
        exe().start(imweb, para)

        # processed_img = imgPlus.img
        processed_imgPlus = imweb.get_img()
        processed_img = processed_imgPlus.img
        new_roi = processed_imgPlus.roi
        print("processed_img = ", processed_img.shape)

        geom = None
        if new_roi:
            # print("new roi = ", new_roi)

            geom = new_roi.to_json()
            # print("geom2shp = ", geom2shp(new_roi.to_geom()))

        # geom_test = {'type': 'GeometryCollection', 'geometries': [{'type': 'MultiPoint', 'coordinates': ((1.0, 73.0, 22.0), (1.0, 134.0, 53.0), (1.0, 179.0, 71.0), (1.0, 413.0, 133.0), (1.0, 251.0, 135.0), (1.0, 557.0, 138.0), (1.0, 492.0, 142.0), (1.0, 140.0, 147.0), (1.0, 50.0, 162.0), (1.0, 38.0, 168.0), (1.0, 190.0, 172.0), (1.0, 144.0, 190.0), (1.0, 77.0, 199.0), (1.0, 42.0, 213.0), (1.0, 175.0, 216.0))}]}

        
        feature = geojson.Feature(geometry=geom)
        feature_collection = geojson.FeatureCollection([feature])
        # print("feature = ", feature_collection)

        feature_collection4canvas = geojson.utils.map_tuples(lambda c: (c[0], img.shape[0]-c[1]), feature_collection)
        roijson_returned = geojson.dumps(feature_collection4canvas)
        # print("new_point = ", roijson_returned)

        #################### test 1 ########################

        # img_dimensions = str(img.shape)
        # return_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # return_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        # return_img = img
        #################### end of test 1 ########################

        buffered = BytesIO()
        processed_pil_img = PILImage.fromarray(processed_img)
        processed_pil_img.save(buffered, format="PNG")
        encoded_img = base64.b64encode(buffered.getvalue()).decode('ascii')

        return {
            'filename': file.filename,
            'dimensions': {
                'height': processed_img.shape[0],
                'width': processed_img.shape[1],
                'channels': 1 if processed_img.ndim==2 else processed_img.shape[2]
            },
            'encoded_img': 'data:image/png;base64,{}'.format(encoded_img),
            'roi': roijson_returned if new_roi else None
        }

    # handling error
    # https://www.runoob.com/python/python-exceptions.html
    # https://fastapi.tiangolo.com/tutorial/handling-errors/#re-use-fastapis-exception-handlers
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
