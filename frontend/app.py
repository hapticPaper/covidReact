from flask import Flask, render_template, send_from_directory, request
from flask_cors import CORS
from sqlalchemy import create_engine
from frontend.queries import sqlite_metrics as Q
import os 

app = Flask(__name__)
CORS(app)

@app.route('/covid.gif')
def covidGif():
    return send_from_directory(os.path.join('..','data'), 'covid.gif')

@app.route('/favicon.ico')
def covidGif():
    return send_from_directory('static', 'favicon.ico')

    
@app.route('/')
def index():
    return render_template('/index.html')

if __name__=='__main__':
    app.run(threaded=True, port=os.environ['PORT'])
