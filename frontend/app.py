from flask import Flask, render_template, send_from_directory, request
from flask_cors import CORS
from sqlalchemy import create_engine
try:
    from frontend.queries import sqlite_metrics as Q
    from frontend.db_loader.lite_loader import exeSql
except: 
    from queries import sqlite_metrics as Q
    #from db_loader.lite_loader import exeSql
import os 
import pymongo


client = pymongo.MongoClient(f"mongodb+srv://rusty:{os.getenv('mongoPass')}@rustydumpster-gtmip.gcp.mongodb.net/rustyDB?retryWrites=true&w=majority")
mongoCovid = client.covid20

app = Flask(__name__)
CORS(app)


DB_PATH = 'frontend/data/db/'
DB_FILE = 'covid.sqlite'
ENG = create_engine(f'sqlite:///{os.path.join(DB_PATH, DB_FILE)}')

@app.route('/latestCovid')
def latestCovid():
    data = exeSql(ENG, Q['latestCovid'])
    return {'results':[{ 'locale':locale, 'confirmed':confirmed, 'deaths':deaths} for locale, confirmed, deaths in data]}

@app.route('/atlasCovid')
def atlasCovid():
    data = mongoCovid.daily.find().sort('cases' ,-1 )[:25]
    dt = mongoCovid.daily.find_one()['refreshed']
    return {'refreshed':dt,'results':[{ 'locale':f"{r['countryRegion']}, {r['provincestate']}", 'cases':r['cases'], 'deaths':r['deaths']} for r in data]}


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

    
@app.route('/')
def index():
    return render_template('/index.html')

if __name__=='__main__':
    app.run(threaded=True, port=os.environ['PORT'])
