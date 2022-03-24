from apiflask import APIFlask
from flask_cors import CORS

app = APIFlask(__name__)
CORS(app)


@app.get('/')
def index():
    return {'message': 'hello world!'}