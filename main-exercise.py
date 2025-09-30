# import package
from fastapi import FastAPI, HTTPExeption
import psycopg2
import pandas as pd

# create FastAPI object
app = FastAPI()

# api key
password = "ranggaimut"

#------------------------------------------------------------------------------------------------------------
def getConnection():
    # create connection
    conn = psycopg2.connect(
        dbname="neondb", user="neondb_owner", password="npg_sLfVg8iW4EwO",
        host="ep-steep-water-a102fmjl-pooler.ap-southeast-1.aws.neon.tech",
    )

    return conn

#-------------------------------------------------------------------------------------------------------------
# endpoint -> untuk mengambil data halaman utama
# @ = simbol decorator
@app.get('/')
def getWelcome(): # function handler
    return {
        "msg": "sample-fastapi-pg"
    }
#-------------------------------------------------------------------------------------------------------------
@app.get('/profile')
def getProfiles():
    # define connection
    connection = getConnection()
    # get data dari database
    df = pd.read_sql("select * from profiles", connection)

    return {
        "data": df.to_dict(orient="records") # dataframe dalam bentuk dictionary -> .to_dict

    }

#------------------------------------------------------------------------------------------------------------
@app.get('/profiles/{id}/{name}')
def getProfileById(id: int, name: str, api_key: str = Header(None)):
    # cek credential
    if api_key == None and api_key != password:
        # kasih error
        raise
    # define connection
    connection = getConnection()
    # get data dari database
    df = pd.read_sql(f"select * from profiles where id = {id}", connection)
    # filter
    df =df.query(f"id == {id} and name == '{name}'")

    if len(df) == 0:
        raise HTTPExeption(status_code=404, detail="data not found")

    return {
        "data": df.to_dict(orient="records"), # dataframe dalam bentuk dictionary -> .to_dict()
        "columns": list(df.columns)
    }



#-------------------------------------------------------------------------------------------------------------
# @app.post(...)
# async def createProfile():
#     pass


#-------------------------------------------------------------------------------------------------------------

# @app.patch(...)
# async def updateProfile():
#     pass

#-------------------------------------------------------------------------------------------------------------

# @app.delete(...)
# async def deleteProfile():
#     pass
