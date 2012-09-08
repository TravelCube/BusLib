from helpers import stops
from helpers import place
from helpers import rides
from helpers import bus_calendar
from helpers import routes
from helpers import trips
import csv
import time


#def import_trips_csv():
#    f = csv.reader(open('/home/omer/tranz/gith/Bus/RwaData/trips.txt'))
#    res = {}
#    f.next()
#    for row in f:
#        res[row[2]] = (tuple(row))
#    return res
#
#trips = import_trips_csv()

def find(bus,lat,lon,acc,hour,day):
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
    res = trips.get_routes(t3)
    #for a in set(t1).intersection(set(t2)).intersection(set(t3)).intersection(set(t4)):
    #    self.ids[a] = 0
    #return self.ids.keys()
    print len(res)
    print time.time() - t
    return res

def get_long_names(l):
    routesIds = set([x[0] for x in l])
    return routes.get_long_names(routesIds)

class user:
    def __init__(self, lat, lon, acc, bus_num):
        self.lat = lat
        self.lon = lon
        self.acc = acc
        self.bus_num = bus_num
        self.ids = {}

    def find(self):
        t1 = routs.find(self.bus_num)
        print len(t1)
        t2 = bus_calendar.find('sunday')
        print len(t2)
        t3 = place.find(self.lat,self.lon,self.acc)
        print len(t3)
        t4 = rids.find('22:00:00')
        print len(t4)
        trips = set(t1).intersection(set(t2)).intersection(set(t3)).intersection(set(t4))
        res = trips.get_routes(trips)
        #for a in set(t1).intersection(set(t2)).intersection(set(t3)).intersection(set(t4)):
        #    self.ids[a] = 0
        #return self.ids.keys()
        return res
    
    def fill_info(self):
        print len(self.ids.keys())
        for key in self.ids.keys():
            self.ids[key] = trips[key][0]

    def get_long_names(self,l):
        routesIds = set([x[0] for x in l])
        return routes.get_long_names(routesIds)
        #l = dict(routs.get_long_names(set(self.ids.values())))
        #self.names_ids = l
        #names = set(l.values())
        #names = dict(zip(range(0,len(names)),names))
        #self.names = names
        #return names 

    def set_long_name(self,long_name_id):
        name = self.names[long_name_id]
        routes_ids = [a[0] for a in res.names_ids.items() if a[1] == name]
        return [a[0] for a in res.ids.items() if int(a[1]) in routes_ids]

    def place_dummy(self):
        import pickle
        s = ['69174702\xd7\x96300712', '14037861\xd7\xa3300712', '69173972\xd7\x96300712', '14037851\xd7\xa3190812', '21017141\xd7\x96270812', '21126801\xd7\x96190812', '21126681\xd7\x96190812', '69174282\xd7\x96300712', '66651552\xd7\x96190812', '66650622\xd7\x96190812', '69175312\xd7\x96300712', '66651452\xd7\x96190812', '21126841\xd7\x96300712', '69175222\xd7\x96300712', '69174952\xd7\x96300712', '66652152\xd7\x96190812', '66651312\xd7\x96190812', '21017311\xd7\x96270812', '14040012\xd7\x9b300712', '21126721\xd7\x96300712', '21017281\xd7\x96270812', '21126691\xd7\x96190812', '66652362\xd7\x96190812', '66651542\xd7\x96190812', '66651522\xd7\x96190812', '66651112\xd7\x96190812', '69174532\xd7\x96300712', '21017191\xd7\x96270812', '21126861\xd7\x96190812', '21126931\xd7\x96190812', '21126851\xd7\x96300712', '21126771\xd7\x96190812', '21126661\xd7\x96190812', '66651662\xd7\x96190812', '69174202\xd7\x96300712', '66650832\xd7\x96190812', '21126971\xd7\x96300712', '21126671\xd7\x96190812', '66651102\xd7\x96190812', '21017181\xd7\x96270812', '21126841\xd7\x96190812', '69174582\xd7\x96300712', '69174412\xd7\x96300712', '66652252\xd7\x96190812', '66651052\xd7\x96190812', '21126671\xd7\x96300712', '21126821\xd7\x96300712', '21126691\xd7\x96300712', '69173982\xd7\x96300712', '21126701\xd7\x96190812', '14037851\xd7\xa3300712', '21126901\xd7\x96190812', '21126791\xd7\x96300712', '21017121\xd7\x96270812', '66651352\xd7\x96190812', '21126881\xd7\x96190812', '21017421\xd7\x96270812', '14037841\xd7\xa3190812', '21126951\xd7\x96190812', '69175062\xd7\x96300712', '69173662\xd7\x96300712', '21017341\xd7\x96270812', '69173522\xd7\x96300712', '21126881\xd7\x96300712', '21126631\xd7\x96190812', '21126781\xd7\x96190812', '69174822\xd7\x96300712', '21017391\xd7\x96270812', '66651782\xd7\x96190812', '66651142\xd7\x96190812', '69175012\xd7\x96300712', '21126781\xd7\x96300712', '66651982\xd7\x96190812', '69175052\xd7\x96300712', '21017381\xd7\x96270812', '21126911\xd7\x96300712', '66651322\xd7\x96190812', '21017301\xd7\x96270812', '21126621\xd7\x96300712', '69174002\xd7\x96300712', '66651642\xd7\x96190812', '21126741\xd7\x96300712', '66651992\xd7\x96190812', '69173892\xd7\x96300712', '21017361\xd7\x96270812', '21017271\xd7\x96270812', '21126821\xd7\x96190812', '69174122\xd7\x96300712', '21017321\xd7\x96270812', '69173872\xd7\x96300712', '21126631\xd7\x96300712', '69174522\xd7\x96300712', '21126971\xd7\x96190812', '14037841\xd7\xa3300712', '21017371\xd7\x96270812', '66650882\xd7\x96190812', '21017231\xd7\x96270812', '21126901\xd7\x96300712', '21126961\xd7\x96190812', '21017161\xd7\x96270812', '21017351\xd7\x96270812', '69175292\xd7\x96300712', '21126861\xd7\x96300712', '21017251\xd7\x96270812', '66651892\xd7\x96190812', '21126921\xd7\x96300712', '21017211\xd7\x96270812', '21126911\xd7\x96190812', '14037851\xd7\xa3270812', '66650562\xd7\x96190812', '21017201\xd7\x96270812', '20973782\xd7\x98190812', '21126641\xd7\x96190812', '21126711\xd7\x96190812', '66651762\xd7\x96190812', '66651152\xd7\x96190812', '21126921\xd7\x96190812', '21126831\xd7\x96190812', '21126661\xd7\x96300712', '21126651\xd7\x96190812', '21017151\xd7\x96270812', '21017091\xd7\x96270812', '21017261\xd7\x96270812', '69175362\xd7\x96300712', '69174492\xd7\x96300712', '21126681\xd7\x96300712', '66651772\xd7\x96190812', '21126951\xd7\x96300712', '21126741\xd7\x96190812', '69174972\xd7\x96300712', '21017411\xd7\x96270812', '21126641\xd7\x96300712', '69175032\xd7\x96300712', '20973782\xd7\x98300712', '21126751\xd7\x96190812', '21017221\xd7\x96270812', '21017171\xd7\x96270812', '69173932\xd7\x96300712', '69174872\xd7\x96300712', '21126761\xd7\x96190812', '21017101\xd7\x96270812', '21126751\xd7\x96300712', '69174852\xd7\x96300712', '21126731\xd7\x96190812', '21017241\xd7\x96270812', '21126771\xd7\x96300712', '21126961\xd7\x96300712', '21017431\xd7\x96270812', '21126791\xd7\x96190812', '69173952\xd7\x96300712', '21126711\xd7\x96300712', '21126721\xd7\x96190812', '66651852\xd7\x96190812', '14037861\xd7\xa3190812', '21126871\xd7\x96190812', '21126801\xd7\x96300712', '69174272\xd7\x96300712', '66651632\xd7\x96190812', '21017291\xd7\x96270812', '21126701\xd7\x96300712', '69175072\xd7\x96300712', '69174262\xd7\x96300712', '21126761\xd7\x96300712', '14037841\xd7\xa3270812', '21126651\xd7\x96300712', '21017081\xd7\x96270812', '66651652\xd7\x96190812', '21126831\xd7\x96300712', '21126851\xd7\x96190812', '21017111\xd7\x96270812', '21017401\xd7\x96270812', '21126621\xd7\x96190812', '21126871\xd7\x96300712', '66651512\xd7\x96190812', '21126811\xd7\x96300712', '66652262\xd7\x96190812', '21126941\xd7\x96300712', '66651302\xd7\x96190812', '21017331\xd7\x96270812', '66651232\xd7\x96190812', '21126811\xd7\x96190812', '21126941\xd7\x96190812', '21126931\xd7\x96300712', '69175162\xd7\x96300712', '14037861\xd7\xa3270812', '21126731\xd7\x96300712', '66651922\xd7\x96190812', '21126891\xd7\x96300712', '14040012\xd7\x9b190812', '21017131\xd7\x96270812', '21126891\xd7\x96190812']

        #l = pickle.loads(s)
        res = trips.get_routes(s)
        return res

def get(bus,lat,lon,acc,hour,day):
    f = open('/home/omer/log.log','w')
    f.write(','.join((bus,lat,lon,acc,hour,day)))
    f.close()
    r = find(bus,lat,lon,acc,hour,day)
    #r = res.place_dummy()
    names = get_long_names(r)
    return names,r

# ids = res.set_long_name(0)

#routs_ids = [trips[x][0] for x in r]
#routs_ids = set(routs_ids)
#print len(routs_ids)

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
    import csv
    from os import path
    l = rides.get_stop_files(trips_ids)
    files = '/home/omer/tranz/gith/Bus/files'
    if len(l) > 1:
        pass
        #erro
    f = csv.reader(open(path.join(files,l[0])))
    l = []
    for r in f:
        l.append(r)
    l = add_lat_lon(l)
    return l
