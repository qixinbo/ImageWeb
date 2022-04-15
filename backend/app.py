from apiflask import APIFlask
from flask_cors import CORS
from flask import jsonify

app = APIFlask(__name__)
CORS(app)

demo = [    
    {
      "name": "前端三大框架",
      "path": "前端三大框架", 
      "children": [
        {
          "name": "vue页面",
          "path": "/vue",
          "children": [],
        },
        {
          "name": "react页面",
          "path": "/react",
          "children": [],
        },
      ],
    },
    {
      "name": "后端三大框架",
      "path": "后端三大框架", 
      "children": [
        {
          "name": "vue页面",
          "path": "/vue",
          "children": [],
        },
      ],
    },
  ]

@app.get('/')
def index():
    return jsonify(demo)

class P:
    def __init__(self, name):
        self.name = name

    def start(self, app):
        print(self.name)
        # print

    def __call__(self):
        return self
    
data = ('menu', [
            ('File', [
                ('Open', P('O')),
                ('Close', P('C'))]),
            ('Edit', [
                ('Copy', P('C')),
                ('A', [
                    ('B', P('B')),
                    ('C', P('C'))]),
                ('Paste', P('P'))])])

data_dict = {'menu': [
              {'File': [
                  {'Open': P('Ohh')},
                  {'Close': P('C')}]}
              ]
              }


import json
from JsonPathFinder import JsonPathFinder
# finder = JsonPathFinder(json.dumps(data_dict, default=lambda obj: obj.__dict__))
finder = JsonPathFinder(data_dict)
path_list = finder.find_one('Close')
# print('0000')          
print('path = ',path_list)



@app.get('/t')
def test():
    return json.dumps(data, default=lambda obj: obj.__dict__)

@app.get('/d')
def test2():
    return json.dumps(data_dict, default=lambda obj: obj.__dict__)

@app.get('/plugins/<p>')
def plugin(p):
  # print('p=',p)
  pl = finder.find_one(p)
  path_list = data_dict[pl[0]][pl[1]][pl[2]][pl[3]]
  path_list[pl[4]].start('a')
  return jsonify(pl)