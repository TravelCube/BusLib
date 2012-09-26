from helpers import stops
from helpers import place
from helpers import rides
from helpers import bus_calendar
from helpers import routes
from helpers import model
from helpers import trips
from helpers import db
import csv
import time
import csv
from os import path

def find(bus,lat,lon,acc,hour,day):
    """ finds the trip ids that mach the args - args are like in get()

    return a list of route id, trip id 
    """
    t1 = time.time()
    t = time.time()
    # data = {agancy: {diraction: {file_nmae : trip_ids}}}
    data = db.get_data(bus)
    print time.time() - t
    t = time.time()
    if len(data.agencies) > 1:
        agency = find_agancy(data,lat,lon,acc,hour,day)
        print 'db'
    else:
        agency = data.agencies.iteritems().next()[1]

    print time.time() - t
    t = time.time()
    if len(agency.diractions[0].file_names) > 1:
        diraction0 = find_file_name(agency.diractions[0],lat,lon,acc,hour,day)
        print 'db'
    else:
        diraction0 = agency.diractions[0].file_names.iteritems().next()[0]

    print time.time() - t
    t = time.time()
    if len(agency.diractions[1].file_names) > 1:
        diraction1 = find_file_name(agency.diractions[1],lat,lon,acc,hour,day)
        print 'db'
    else:
        diraction1 = agency.diractions[1].file_names.iteritems().next()[0]

    print time.time() - t
    print time.time() - t1
    return [diraction0,diraction1]

def find_agancy(data,lat,lon,acc,hour,day):
    for agency,obj in data.agencies.items():
        trip_ids = obj.get_all_trip_ids()
        trip_ids = bus_calendar.find(day,trip_ids)
        if len(trip_ids) == 0:
            continue
        trip_ids = rides.find(hour, trip_ids)
        if len(trip_ids) == 0:
            continue
        if place.find_first(lat,lon,acc,trip_ids):
            return obj

def find_file_name(diraction,lat,lon,acc,hour,day):
    for file_name,obj in diraction.file_names.items():
        trip_ids = obj.trip_ids
        trip_ids = bus_calendar.find(day,trip_ids)
        if len(trip_ids) == 0:
            continue
        trip_ids = rides.find(hour, trip_ids)
        if len(trip_ids) == 0:
            continue
        if place.find_first(lat,lon,acc,trip_ids):
            return file_name

def get_trips_stops(trip_ids):
    """ find the stops files and the last station name for the trip ids

    return distinct list of stop_file, last station
    """
    l = stops.get_stop_files_last_station(trip_ids)
    return l

def get(bus,lat,lon,acc,hour,day):
    """return the lines thact match the args

    args:
    bus -- bus number
    lat,lon -- latitude, longitude
    acc -- accurcie of the cordint
    hour -- 2 digit of the hour now (that can be diffrent in client server, and we need the client)
    dat -- the day in words (also can be diffrent in client-server)

    return:
        1. list of route id, route name
        2. list od trip id, route id
    """
    r = find(bus,lat,lon,acc,hour,day)
    r = get_trips_stops(r)
    return r

def get_ids(stops):
    ids = [x[0] for x in stops]
    return ids

def add_lat_lon(stopscsv):
        d = stops.get_stops_lat_lon(get_ids(stopscsv))
        res = []
        for row in stopscsv:
           res.append(row + list(d[int(row[0])]))
        return res

def get_stops(file_name):
    """ return list of stops for the trip id"""
    files = '/home/omer/tranz/gith/Bus/new_files'
    f = csv.reader(open(path.join(files,file_name)))
    l = []
    for r in f:
        l.append(r)
    l = add_lat_lon(l)
    return l
