from flask import Flask, render_template, send_from_directory, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('/index.html')

if __name__=='__main__':
    sched.start()
    app.run()
