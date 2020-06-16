import requests, json, datetime
from frontend.db_loader.fieldmappings import mappings
import logging as l



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



def fetchCovidData(engine):
    resp = requests.get('https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv')
    try:
        data = resp.content.decode("utf8").replace("\r","").replace("'","").split("\n")
        trunctate(engine)
        insertFile(data, engine)
        exeSql(engine, UPDATE_KEY)
        return data or resp.status_code
    except Exception as e:
        l.critical(f"Somethign failed - {e}")