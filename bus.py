from helpers import stops
from helpers import place
from helpers import rides
from helpers import bus_calendar
from helpers import routes
from helpers import trips
import csv
import time
import csv
from os import path

def find(bus,lat,lon,acc,hour,day):
    """ finds the trip ids that mach the args - args are like in get()

    return a list of route id, trip id 
    """
    t = time.time()
    t1 = routes.find(bus)
    print len(t1)
    t2 = bus_calendar.find(day)
    print len(t2)
    ids = set(t1).intersection(set(t2))
    t4 = rides.find(hour,ids)
    print len(t4)
    t3 = place.find(lat,lon,acc,t4)
    print len(t3)
    #res = trips.get_routes(t3)
    #print len(res)
    print time.time() - t
    return t3

def get_trips_stops(trip_ids):
    """ find the stops files and the last station name for the trip ids

    return distinct list of stop_file, last station
    """
    l = stops.get_stop_files_last_station(trip_ids)
    return l

def get_long_names(l):
    """ find the route name for the route ids, return distinct list

    args:
    l -- a list route id ...

    return distnict list, route id and route name
    """
    routesIds = set([x[0] for x in l])
    return routes.get_long_names(routesIds)

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
    #names = get_long_names(r)
    return r

def get_ids(stops):
    ids = [x[2] for x in stops]
    return ids

def add_lat_lon(stopscsv):
        d = stops.get_stops_lat_lon(get_ids(stopscsv))
        res = []
        for row in stopscsv:
           res.append(row + list(d[int(row[2])]))
        return res

def get_stops(trips_ids):
    """ return list of stops for the trip id"""
    l = rides.get_stop_files(trips_ids)
    files = '/home/omer/tranz/gith/Bus/new_files'
    if len(l) > 1:
        pass
        #erro
    f = csv.reader(open(path.join(files,l[0])))
    l = []
    for r in f:
        l.append(r)
    l = add_lat_lon(l)
    return l
