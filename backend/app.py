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