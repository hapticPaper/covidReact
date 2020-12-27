import requests, json, datetime, pandas, time
try:
    from frontend.db_loader.fieldmappings import mappings
except:
    from fieldmappings import mappings
import os
import pymongo


client = pymongo.MongoClient(f"mongodb+srv://rusty:{os.getenv('mongoPass')}@rustydumpster-gtmip.gcp.mongodb.net/rustyDB?retryWrites=true&w=majority")
mongoCovid = client.covid20

def insertMany(data, table):
    return table.insert_many(data)

def exeSql(engine, sql):
    return engine.execute(sql)

DATES=f"""SELECT distinct date(lastupdate) date from  us_daily where date(lastUpdate) is not null order by 1"""
dt = datetime.datetime.today() #(2020,4,9)
DT = dt.strftime('%Y%m%d') #'20200322' #
DATEY = dt.strftime('%Y-%m-%d')


def GET_COLUMNS(line):
    return f"({', '.join([mappings[i] for i in line.split(',')])})"

def INSERT(fields, values):
    return f"""INSERT INTO daily {fields}
               VALUES {str(values)}
    """
UPDATE_KEY = """
UPDATE daily SET combinedkey = replace(replace(case
			when admin2 is not null then admin2|| ', '|| provincestate||', '|| countryregion
			when provincestate is not null then provincestate||', '|| countryregion
	  		else countryregion
	  end, 'Unassigned, ', ''), 'unassigned','')
  WHERE combinedkey is null;
  """
def writeMongo(data, table):
    fields = [mappings[i] for i in data[0].split(",")]
    cdata = pandas.DataFrame([dict(zip(fields, d.split(","))) for d in data[1:]])
    cdata.deaths = pandas.to_numeric(cdata.deaths)
    cdata.cases = pandas.to_numeric(cdata.cases)
    try:
        cdata.confirmed_deaths = pandas.to_numeric(cdata.confirmed_deaths)
        cdata.confirmed_cases = pandas.to_numeric(cdata.confirmed_cases)
        cdata.probable_deaths = pandas.to_numeric(cdata.probable_deaths)
        cdata.probable_cases = pandas.to_numeric(cdata.probable_cases)
    except Exception as e:
        print(f"Field not found - {e}")
    cdata['refreshed'] = time.time()
    return insertMany(json.loads(cdata.to_json(orient='records')), table)



def insertFile(data, conn):
    tuples = []
    fields = GET_COLUMNS(data[0])
    values = data[1:]
    for record in values:
        r = record.split(',')
        if len(r)==len(fields.split(",")):
            tuples.append(f"""({','.join([f"'{d}'" for d in r])})""")
    values = ",\n".join(tuples)
    r = conn.execute(INSERT(fields, values))
    print(r)
    return r

def truncateMongo(mongo_obj):
    return mongo_obj.delete_many({}).deleted_count

def trunctate(engine):
    print("\n\nTruncating daily")
    exeSql(engine, """DROP TABLE IF EXISTS daily;""")
    exeSql(engine,"""
    create table daily
    (
        FIPS          integer,
        Admin2        character varying,
        provinceState character varying,
        countryRegion character varying,
        lastUpdate    timestamp,
        lat           double precision,
        lng           double precision,
        confirmed     bigint,
        probableconfirmed bigint,
        probabledeaths bigint,
        deaths        bigint,
        recovered     bigint,
        active        bigint,
        incidentrate  double precision,
        testingrate  double precision,
        fatalityrate  double precision,
        peopletested  bigint,
        hospitalized  bigint,
        hospitilizationrate  double precision,
        mortalityrate  double precision,
        combinedKey   character varying,
        UID   character varying,
        ISO3   character(3)
    );


    """)

def loadMongoCSV(resp,mongoObj, truncate=True):
    try:
        data = resp.content.decode("utf8").replace("\r","").replace("'","").split("\n")   

        if truncate:
             truncateMongo(mongoObj)
        writes = writeMongo(data, mongoObj)
        print(f"Mongo writes: {len(writes.inserted_ids)}")
        return data or resp.status_code
    except Exception as e:
            print(f"Somethign failed - {e}")
            return e

def getUsTotals():
    resp = requests.get('https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us.csv')
    loadMongoCSV(resp, mongoCovid.usTotal)


def fetchCountyData():
    resp = requests.get('https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv')
    data = loadMongoCSV(resp, mongoCovid.counties)
    return data

def fetchDailyData():
    resp = requests.get('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
    
    with open('daily.csv','w') as d:
        d.write(resp.content.decode('latin-1'))
    df = pandas.read_csv('daily.csv', sep=',')
    return df


if __name__=='__main__':
    #fetchCountyData()
    #getUsTotals()
    sdf=fetchDailyData()



    sdf['combinedKey'] = sdf['county']+", "+sdf['state']
    {d:sdf.loc[sdf.date==d][['combinedKey', 'cases', 'deaths']].to_dict('records') for d in sorted(set(sdf['date']))}