from flask import Flask
import os
import sqlalchemy
from yaml import load, Loader

from sqlalchemy import DDL, event, MetaData, Table, Column, Integer, String, Sequence
from sqlalchemy.ext.compiler import compiles
from flask_sqlalchemy import SQLAlchemy

def init_connect_engine():
    if os.environ.get('GAE_ENV') != 'standard':
        variables = load(open("app.yaml"), Loader=Loader)
        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]
    
    pool = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername="mysql+pymysql",
                username=os.environ.get('MYSQL_USER'),
                password=os.environ.get('MYSQL_PASSWORD'),
                database=os.environ.get('MYSQL_DB'),
                host=os.environ.get('MYSQL_HOST')
            )
        )
    return pool


app = Flask(__name__)
db = init_connect_engine()

#############TRIGGER#########################
META_DATA = MetaData(bind=db)
META_DATA.reflect()
SONG_TRENDS_TABLE = META_DATA.tables['SongTrends']

trigger = DDL('''\
    CREATE TRIGGER song_insert_trig BEFORE INSERT ON SongTrends 
        FOR EACH ROW BEGIN
        IF NEW.song_id NOT IN (SELECT DISTINCT SongTrends.song_id FROM SongTrends) THEN
        UPDATE Trends 
            SET recent_song_id = new.song_id WHERE Trends.trend_name = new.trend_name;
        END IF;
    END;
    ''')

# event listener to trigger on data insert to MyTable
event.listen(SONG_TRENDS_TABLE, "after_create", trigger)



from app import routes

