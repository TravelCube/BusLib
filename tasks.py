from celery import task
from datetime import datetime
import place

@task()
def add(x,y):
    return x+y

@task(name ="android.Bus.tasks.check")
def check(agency, userd):
    false_list = []
    trips = agency.get_all_trip_ids()
    trips = check_services(trips,userd.service_ids)
    if len(trips) == 0:
        return False, false_list
    trips = check_start_time(trips,userd.hour)
    if len(trips) == 0:
        return False, false_list
    shape_ids = [x.shape_id for x in trips]
    res,false_list =  place.find_first(userd.lat,userd.lon,userd.acc,shape_ids, false_list)
    if res == True:
        return agency, false_list
    else:
        return False, false_list

def check_services(trips,service_ids):
    """ return the trips that there service_id is in the list: service_ids
        return [] for defaulte
    """
    res = []
    for t in trips:
        if t.service_id in service_ids:
            res.append(t)
    return res

def check_start_time(trips,hour):
    hour = datetime.strptime(hour,'%H:%M:%S')
    res = []
    for t in trips:
        st = datetime.strptime(t.start_time,'%Y-%m-%d %H:%M:%S')
        if hour > st:
            res.append(t)
    return res
