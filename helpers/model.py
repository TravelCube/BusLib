import place
import bus_calendar
from datetime import datetime

class agency:
    def __init__(self,number):
        self.agency_id = number
        self.diractions = [diraction(),diraction()]

    def add(self,diraction, *args):
        self.diractions[diraction].add(*args)
    
    def get_all_trip_ids(self):
        res = []
        for d in self.diractions:
            for name in d.file_names.values():
                for v in name.trip_ids.values():
                    res.append(v)
        return res

    def is_agency_match(self, userd, false_list):
        trips= self.get_all_trip_ids()
        trips = check_services(trips,userd.service_ids)
        if len(trips) == 0:
            return False, false_list
        trips = check_start_time(trips,userd.hour)
        if len(trips) == 0:
            return False, false_list
        shape_ids = [x.shape_id for x in trips]
        res,false_list =  place.find_first(userd.lat,userd.lon,userd.acc,shape_ids, false_list)
        if res == True:
            return True, false_list
        else:
            return False, false_list

class file_name:
    def __init__(self):
        self.trip_ids = {}
    
    def add(self,trip_id, *args):
        if trip_id not in self.trip_ids:
            self.trip_ids[trip_id] = c_trip_id()
        self.trip_ids[trip_id].add(trip_id,*args)

    def is_file_name_match(self,userd,false_list):
        trips = self.trip_ids
        trips= check_services(trips,userd.service_ids)
        if len(trips) == 0:
            return False, false_list
        trips = check_start_time(trips,userd.hour)
        if len(trips) == 0:
            return False, false_list
        shape_ids = [x.shape_id for x in trips]
        res,false_list =  place.find_first(user.lat,user.lon,user.acc,shape_ids, false_list)
        if res == True:
            return True, false_list
        else:
            return False, false_list

class diraction:
    def __init__(self):
        self.file_names = {}

    def add(self,name, *args):
        if name not in self.file_names:
            self.file_names[name] = file_name()
        self.file_names[name].add(*args)

    def find_file_name_macth(self,userd, false_list):
        if len(self.file_names) == 1:
             return self.file_names.values()[0], false_list
        else:
            for file_name_obj in self.file_names.values():
                res, false_list = file_name_obj.is_file_name_match(userd, false_list)
                if res:
                    return file_name_obj, false_list
            return None, false_list

class bus_root:
    def __init__(self,num):
        self.bus_number = num
        self.agencies = {}

    def add(self,agency_id,*args):
        if agency_id not in self.agencies:
            self.agencies[agency_id] = agency(agency_id)
        self.agencies[agency_id].add(*args)

    def find_agency(self,userd, false_list):
        if len(self.agencies) == 1:
            return self.agencies.values()[0], false_list
        else:
            for agency in self.agencies.values():
                res,false_list = agency.is_agency_match(userd, false_list)
                if res:
                    return agency, false_list
            return None

    def find_file_names(self,userd):
        false_list = []
        magency,false_list = self.find_agency(userd,false_list)
        if magency == None:
            return None

        file_name0, false_list = magency.diractions[0].find_file_name_macth(userd, false_list)
        file_name1, false_list = magency.diractions[1].find_file_name_macth(userd, false_list)
        return (file_name0, file_name1)

class c_trip_id:
    def __init__(self):
        self.start_time = None
        self.service_id = None
        self.shape_id = None

    def add(self,tid,service_id, start_time, shape_id):
        self.start_time = start_time
        self.service_id = service_id
        self.tid = tid
        self.shape_id = shape_id

class user_data:
    def __init__(self, lat, lon, acc, hour, day):
        self.lat = lat
        self.lon = lon 
        self.acc = acc 
        self.hour = hour 
        self.service_ids = bus_calendar.get_ids(day)

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
