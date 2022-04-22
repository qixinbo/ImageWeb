from apiflask import APIFlask
from flask_cors import CORS
from flask import jsonify, request

app = APIFlask(__name__)
CORS(app)

class P:
    def __init__(self, name):
        self.name = name

    def start(self, app):
        print(self.name)
        # print

    def __call__(self):
        return self
    
data_v1 = ('menu', [
            ('File', [
                ('Open', P('O')),
                ('Close', P('Close'))]),
            ('Edit', [
                ('Copy', P('Copy')),
                ('A', [
                    ('B', P('B')),
                    ('C', P('C'))]),
                ('Paste', P('P'))])])


data_dict = {'menu': {
              'File': {
                  'Open': P('O'),
                  'Close': P('close'),
                  },
                
              'Edit': {
                  'Copy': P('Copy'),
                  'A': {
                    'B': P('B'),
                    'C': P('C')
                  },
                  }
              },
              }


print('----------- testD -----------------')

data_v2 = [
            ('File', [
                ('Open', P('O')),
                ('Close', P('Close'))]),
            ('Edit', [
                ('Copy', P('Copy')),
                ('A', [
                    ('B', P('B')),
                    ('C', P('C'))]),
                ('Paste', P('P'))])]

# print(dict(data_v2))
# print(data_dict['menu']['Edit']['A'])

import json

p= ["Edit", "A", "B"]

def find_exe(data, p):
    if len(p) > 1:
        data = data[p[0]]
        p.pop(0)
        exe = find_exe(data, p)
        return exe
    elif len(p) == 1:
        return data[p[0]]
    else:
        return None


exe = find_exe(data_dict['menu'], p)
# print('exe = ', exe)

import imagepy
from imagepy.app import ImageWeb

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

flatten(menus)


@app.get('/t')
def test():
    # return json.dumps(data_dict, default=lambda obj: obj.__dict__)
    return json.dumps(flatten(menus)[1], default=lambda obj: obj.__dict__)

@app.post('/plugins/')
def plugin():
    print('p=', request.json)
    exe = find_exe(data_dict['menu'], request.json)
    return jsonify(exe.start('app'))


