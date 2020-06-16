from flask import Flask, render_template, send_from_directory, request
from flask_cors import CORS
from sqlalchemy import create_engine
from frontend.queries import sqlite_metrics as Q
from frontend.db_loader.lite_loader import exeSql
import os 

app = Flask(__name__)
CORS(app)


DB_PATH = 'frontend/data/db/'
DB_FILE = 'covid.sqlite'
ENG = create_engine(f'sqlite:///{os.path.join(DB_PATH, DB_FILE)}')

@app.route('/latestCovid')
def latestCovid():
    data = exeSql(ENG, Q['latestCovid'])
    return {'results':[{ 'locale':locale, 'confirmed':confirmed, 'deaths':deaths} for locale, confirmed, deaths in data]}


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

    
@app.route('/')
def index():
    return render_template('/index.html')

if __name__=='__main__':
    app.run(threaded=True, port=os.environ['PORT'])
