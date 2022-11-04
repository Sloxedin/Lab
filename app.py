from flask import Flask
from waitress import serve

app = Flask(__name__)

# http://127.0.0.1:5000/api/v1/hello-world-10
@app.route('/api/v1/hello-world-10')
def hello_world():
    return "Hello world 10"

if __name__ == '__main__':
    print("Server started")
    serve(app)