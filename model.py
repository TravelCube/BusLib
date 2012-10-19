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
                for v in name.shapes.values():
                    res.append(v)
        return res

    def is_agency_match(self, userd, false_list):
        print self.agency_id
        shapes= self.get_all_trip_ids()
        shapes = check_service_time(shapes,userd.service_ids,userd.hour)
        #shapes = check_services(shapes ,userd.service_ids)
        #if len(shapes) == 0:
        #    print 'f1'
        #    return False, false_list
        #shapes = check_start_time(shapes,userd.hour)
        if len(shapes) == 0:
            print 'f2'
            return False, false_list
        shape_ids = [x.shape_id for x in shapes]
        print 'len',len(shape_ids)
        res,false_list =  place.find_first(userd.lat,userd.lon,userd.acc,shape_ids, false_list)
        if res == True:
            return True, false_list
        else:
            return False, false_list

class file_name:
    def __init__(self):
        self.shapes = {}
    
    def add(self,shape_id, *args):
        if shape_id not in self.shapes:
            self.shapes[shape_id] = shape(shape_id)
        self.shapes[shape_id].add(*args)

    def is_file_name_match(self,userd,false_list):
        shapes = self.shapes.values()
        shapes = check_service_time(shapes,userd.service_ids,userd.hour)
        #shapes= check_services(shapes,userd.service_ids)
        #if len(shapes) == 0:
        #    return False, false_list
        #shapes = check_start_time(shapes,userd.hour)
        if len(shapes) == 0:
            return False, false_list
        shape_ids = [x.shape_id for x in shapes]
        res,false_list =  place.find_first(userd.lat,userd.lon,userd.acc,shape_ids, false_list)
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
             return self.file_names.keys()[0], false_list
        else:
            for file_name,file_name_obj in self.file_names.iteritems():
                res, false_list = file_name_obj.is_file_name_match(userd, false_list)
                if res:
                    return file_name, false_list
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
                print agency
                res,false_list = agency.is_agency_match(userd, false_list)
                print len(false_list)
                if res:
                    return agency, false_list
            return None, []

    def find_file_names(self,userd):
        false_list = []
        magency,false_list = self.find_agency(userd,false_list)
        if magency == None:
            return None

        file_name0, false_list = magency.diractions[0].find_file_name_macth(userd, false_list)
        file_name1, false_list = magency.diractions[1].find_file_name_macth(userd, false_list)
        return (file_name0, file_name1)

class shape:
    def __init__(self, shape_id):
            self.services = []
            self.shape_id =  shape_id

    def add(self,service_id, start_time):
            self.services.append((service_id, start_time))

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
        st = datetime.strptime(t.start_time,'%H:%M:%S')
        print st
        if hour > st:
            res.append(t)
    return res

def check_services(trips,service_ids):
    """ return the trips that there service_id is in the list: service_ids
        return [] for defaulte
    """
    res = []
    for t in trips:
        print t.service_id
        if int(t.service_id) in service_ids:
            res.append(t)
    return res

def check_service_time(shapes, service_ids, hour):
    hour = datetime.strptime(hour,'%H:%M:%S')
    res = []
    for shape in shapes:
        for r in shape.services:
            if int(r[0]) in service_ids:
                if hour > datetime.strptime(r[1],'%H:%M:%S'):
                    res.append(shape)
                    continue
    return res
