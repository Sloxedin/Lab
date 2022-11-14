from flask import Flask
from waitress import serve

app = Flask(__name__)

@app.route('/api/v1/hello-world-10')
def hello_word():
    return "Hello world 10", 200

if __name__ == '__main__':
    print("Server started")
    serve(app)