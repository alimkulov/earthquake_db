import requests
import sqlite3

def setEarthquakeData():
    format= 'geojson' 
    # input('Please enter the format: ')
    starttime= '2019-01-01'
    # input('Please enter the starttime: ')
    endtime='2019-05-01'
    # input('Please enter the endtime: ')
    latitude= '51.51'
    # input('Please enter the latitude: ')
    longitude='-0.12'
    # input('Please enter the longitude: ')
    maxradiuskm=2000
    # input('Please enter the maxradiuskm: ')
    minmagnitude=2
    # input('Please enter the minmagnitude: ')

    url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?'
    response = requests.get(url, headers={'Accept':'application/json'}, params={
            'format': format,
            'starttime':starttime,
            'endtime':endtime,
            'latitude':latitude,
            'longitude':longitude,
            'maxradiuskm':maxradiuskm,
            'minmagnitude':minmagnitude
        })

    data = response.json()

    conn=sqlite3.connect('earthquake_db.db')

    cursor=conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS earthquakes(place TEXT, magnitude REAL);')
    conn.commit()

    insert_query='INSERT INTO earthquakes VALUES(?,?);'

    i=0
    while i<len(data['features']):
        place=data['features'][i]['properties']['place']
        mag=data['features'][i]['properties']['mag']
        earthquake_data=(place,mag)
        cursor.execute(insert_query,earthquake_data)
        i+=1
    print(i)        
    conn.commit()
    conn.close()

def getEarthquakeData():
    conn=sqlite3.connect('earthquake_db.db')
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM earthquakes;")
    print(cursor.fetchall())

    conn.commit()
    conn.close()


setEarthquakeData()
getEarthquakeData()