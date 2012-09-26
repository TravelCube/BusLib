class agency:
    def __init__(self,number):
        self.agency_id = number
        self.diractions = [diraction(),diraction()]
        self.trip_ids = []

    def add(self,diraction,file_name,trip_id):
        self.trip_ids.append(trip_id)
        self.diractions[diraction].add(file_name,trip_id)
    
    def get_all_trip_ids(self):
        return self.trip_ids

class file_name:
    def __init__(self):
        self.trip_ids = []
    
    def add(self,trip_id):
        self.trip_ids.append(trip_id)

class diraction:
    def __init__(self):
        self.file_names = {}

    def add(self,name, trip_id):
        if name not in self.file_names:
            self.file_names[name] = file_name()
        self.file_names[name].add(trip_id)

class bus_root:
    def __init__(self,num):
        self.bus_number = num
        self.agencies = {}

    def add(self,agency_id,diraction,file_name,trip_id):
        if agency_id not in self.agencies:
            self.agencies[agency_id] = agency(agency_id)
        self.agencies[agency_id].add(diraction,file_name,trip_id)
