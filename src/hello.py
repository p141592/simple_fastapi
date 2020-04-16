import os

from flask import Flask

e = os.environ
app = Flask(__name__)

@app.route('/')
def hello_world():
    return e.get('WELCOME_STRING')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
