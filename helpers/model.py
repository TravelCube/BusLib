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

class file_name:
    def __init__(self):
        self.trip_ids = {}
    
    def add(self,trip_id, *args):
        if trip_id not in self.trip_ids:
            self.trip_ids[trip_id] = c_trip_id()
        self.trip_ids[trip_id].add(trip_id,*args)

class diraction:
    def __init__(self):
        self.file_names = {}

    def add(self,name, *args):
        if name not in self.file_names:
            self.file_names[name] = file_name()
        self.file_names[name].add(*args)

class bus_root:
    def __init__(self,num):
        self.bus_number = num
        self.agencies = {}

    def add(self,agency_id,*args):
        if agency_id not in self.agencies:
            self.agencies[agency_id] = agency(agency_id)
        self.agencies[agency_id].add(*args)

class c_trip_id:
    def __init__(self):
        self.start_time = None
        self.service_id = None
        self.stops_ids = None

    def add(self,tid,service_id, start_time):
        self.start_time = start_time
        self.service_id = service_id
        self.tid = tid
