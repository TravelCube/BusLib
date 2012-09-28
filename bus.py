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
from datetime import datetime
from multiprocessing import Pool

def test(num):
    print find(num,'32.306622','34.901074','100.0','10:00:00','sunday')
    print 'old'
    #print find_old(num,'32.306622','34.901074','100.0','10:00:00','sunday')

def find(bus,lat,lon,acc,hour,day):
    """ finds the trip ids that mach the args - args are like in get()

    return a list of route id, trip id 
    """
    false_list = []
    t1 = time.time()
    t = time.time()
    # data = {agancy: {diraction: {file_nmae : trip_ids}}}
    data = db.get_bus(bus)
    print time.time() - t, 'get data'
    t = time.time()
    if len(data.agencies) > 1:
        print 'db'
#        agency, false_list = find_agancy(data,lat,lon,acc,hour,day, false_list)
        agency = new_find_agency(data,lat,lon,acc,hour,day)
    else:
        agency = data.agencies.iteritems().next()[1]

    print time.time() - t, 'agency'
    t = time.time()
    return agency
#
    if len(agency.diractions[0].file_names) > 1:
        print 'db'
        diraction0, false_list = find_file_name(agency.diractions[0],lat,lon,acc,hour,day, false_list)
    else:
        if len(agency.diractions[0].file_names) == 0:
            diraction0 = None
        else:
            diraction0 = agency.diractions[0].file_names.iteritems().next()[0]

    print time.time() - t
    t = time.time()
    if len(agency.diractions[1].file_names) > 1:
        print 'db'
        diraction1, false_list = find_file_name(agency.diractions[1],lat,lon,acc,hour,day, false_list)
    else:
        diraction1 = agency.diractions[1].file_names.iteritems().next()[0]

    print time.time() - t
    print time.time() - t1
    return [diraction0,diraction1]

def find_old(bus,lat,lon,acc,hour,day):
    t = time.time()
    t1 = routes.find(bus)
    print len(t1)
    t2 = bus_calendar.find_all(day)
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

def find_agancy(data,lat,lon,acc,hour,day, false_list):
    false_list = false_list
    for agency,obj in data.agencies.items():
        trips= obj.get_all_trip_ids()
        service_ids = bus_calendar.get_ids(day)
        trips = check_services(trips,service_ids)
        if len(trips) == 0:
            continue
        trips = check_start_time(trips,hour)
        if len(trips) == 0:
            continue
        shape_ids = [x.shape_id for x in trips]
        res,false_list =  place.find_first(lat,lon,acc, shape_ids, false_list)
        if res == True:
            return obj, false_list

def new_find_agency(data,lat,lon,acc,hour,day):
    service_ids = bus_calendar.get_ids(day)
    args = [(x[1],lat,lon,acc,hour,service_ids) for x in data.agencies.items()]
    #for a in args:
    #    agency_check(a)
    it = Pool(processes=10).imap_unordered(agency_check, args)
    for i in range(len(args)):
        print 'i', i
        obj = it.next()
        if obj != None:
            return obj

def agency_check(args):
    obj,lat,lon,acc,hour,service_ids = args
    trips= obj.get_all_trip_ids()
    trips = check_services(trips,service_ids)
    if len(trips) == 0:
        return None
    trips = check_start_time(trips,hour)
    if len(trips) == 0:
        return None
    false_list = []
    shape_ids = [x.shape_id for x in trips]
    res,false_list =  place.find_first(lat,lon,acc,shape_ids, false_list)
    if res == True:
        return obj
    else:
        return None

def check_start_time(trips,hour):
    hour = datetime.strptime(hour,'%H:%M:%S')
    res = []
    for t in trips:
        st = datetime.strptime(t.start_time,'%Y-%m-%d %H:%M:%S')
        if hour > st:
            res.append(t)
    return res

def check_services(trips,service_ids):
    res = []
    for t in trips:
        if t.service_id in service_ids:
            res.append(t)
    return res

def find_file_name(diraction,lat,lon,acc,hour,day, false_list):
    false_list = false_list
    for file_name,obj in diraction.file_names.items():
        trip_ids = obj.trip_ids
        trip_ids = bus_calendar.find(day,trip_ids)
        if len(trip_ids) == 0:
            continue
        trip_ids = rides.find(hour, trip_ids)
        if len(trip_ids) == 0:
            continue
        res,false_list =  place.find_first(lat,lon,acc,trip_ids, false_list)
        if res == True:
            return file_name, false_list
    return None,false_list

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
