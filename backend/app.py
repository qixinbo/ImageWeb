from apiflask import APIFlask
from flask_cors import CORS
from flask import jsonify, request
import json

import imagepy
from imagepy.app import ImageWeb

app = APIFlask(__name__)
CORS(app)

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

# print(menus)

@app.get('/menu')
def test():
    # return json.dumps(data_dict, default=lambda obj: obj.__dict__)
    return json.dumps(flatten(menus)[1], default=lambda obj: obj.__dict__)

@app.post('/plugins/')
def plugin():
    print('p=', request.json)
    exe = imweb.plugin_manager.get(request.json)
    print(exe)
    return "hello world"