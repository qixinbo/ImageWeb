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
print('exe = ', exe)


@app.get('/t')
def test():
    return json.dumps(data_dict, default=lambda obj: obj.__dict__)

@app.post('/plugins/')
def plugin():
    print('p=', request.json)
    exe = find_exe(data_dict['menu'], request.json)
    return jsonify(exe.start('app'))