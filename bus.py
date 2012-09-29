from helpers import stops
from helpers import place
from helpers import rides
from helpers import bus_calendar
#from helpers import routes
#from helpers import model
#from helpers import trips
from helpers import db
import csv
import time
from os import path
from datetime import datetime
from multiprocessing import Pool

def test(num):
    print find(num,'32.306622','34.901074','100.0','10:00:00','sunday')
    print 'old'
    #print find_old(num,'32.306622','34.901074','100.0','10:00:00','sunday')

def find(bus,lat,lon,acc,hour,day):
    """ finds the trip ids that mach the args - args are like in get()

    returns tuple of two files name,
    one for eche diraction.
    one of them can be None.

    if there is no bus match the args - return None
    """
    root = db.get_bus(bus)
    # root is helper.model.bus_root object

    if root == None:
        return None

    if len(root.agencies) > 1:
        agency, false_list = _find_agency(root.agencies,lat,lon,acc,hour,day)
    else:
        agency = root.agencies.iteritems().next()[1]

    if agency == None:
        return None

    if len(agency.diractions[0].file_names) > 1:
        diraction0, false_list = find_file_name(agency.diractions[0],lat,lon,acc,hour,day, false_list)
    else:
        if len(agency.diractions[0].file_names) == 0:
            diraction0 = None
        else:
            diraction0 = agency.diractions[0].file_names.iteritems().next()[0]

    if len(agency.diractions[1].file_names) > 1:
        diraction1, false_list = find_file_name(agency.diractions[1],lat,lon,acc,hour,day, false_list)
    else:
        diraction1 = agency.diractions[1].file_names.iteritems().next()[0]

    return [diraction0,diraction1]

def _find_agency(agencies,lat,lon,acc,hour,day):
    """ private function, finds the agency for the given args
    uses Pool for speed

    return the agency class, if ther isn't return None
    """
    service_ids = bus_calendar.get_ids(day)
    args = [(x[1],lat,lon,acc,hour,service_ids) for x in agencies.items()]
    pool = Pool(processes=len(args)) 
    it = pool.imap_unordered(agency_check, args)
    for i in range(len(args)):
        obj = it.next()
        if obj != None:
            return obj
    return None

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
        return obj, false_list
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
    """ return the trips that there service_id is in the list: service_ids
        return [] for defaulte
    """
    res = []
    for t in trips:
        if t.service_id in service_ids:
            res.append(t)
    return res

def find_file_name(diraction,lat,lon,acc,hour,day, false_list):
    """ finds the file_name that matche the args
    false_list is for the place.find - it is a list of points that alrady been checked
    return tuple: file_name, false_list
    or None, false_list if there isn't file name that matches
    """
    service_ids = bus_calendar.get_ids(day)
    for file_name,obj in diraction.file_names.items():
        trips= obj.trip_ids.values()
        trips= check_services(trips,service_ids)
        if len(trips) == 0:
            continue
        trips = check_start_time(trips,hour)
        if len(trips) == 0:
            continue
        shape_ids = [x.shape_id for x in trips]
        res,false_list =  place.find_first(lat,lon,acc,shape_ids, false_list)
        if res == True:
            return file_name, false_list
    return None,false_list

def _get_files_first_stop(file_names):
    """ find the stops files and the last station name for the trip ids

    return distinct list of stop_file, last station
    """
    l = stops.get_stop_files_last_station(file_names)
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
        tuple of 2 tuples:
            file_name, last stop
        one for eche diraction
    """
    r = find(bus,lat,lon,acc,hour,day)
    r = _get_files_first_stop(r)
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
    #return l
