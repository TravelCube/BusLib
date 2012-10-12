from geopy import distance
import db
from os import path

distance.VincentyDistance.ELLIPOSID = 'WGS-84'
d = distance.distance

def set_stops(rwe_data_path):
    """ return a dict that hold data from stops.txt
        dict[stop_id] = (lat, lon, name, desc)
    """
    f = open(path.join(rwe_data_path, 'stops.txt'), 'r')
    stops = {}
    for row in f:
        row = row.split(',')
        stops[row[0]] = (row[4],row[5], row[2], row[3])
    return stops

def set_trip_stops(rwe_data_path):
    """
        return a dict thats holds the data from stop_times.txt
        dict[trip_id] = [[stop_id,...],start_time]
    """
    res = {}
    b = []
    f = open(path.join(rwe_data_path,'stop_times.txt'), 'r')
    for row in f:
        sp = row.split(',')
        if sp[0] not in res:
            res[sp[0]] = [[],sp[1]]
        res[sp[0]][0].append(sp[3])
        if sp[3] not in stops:
            b.append(sp[3])
    return res, set(b)

def run(diraction, target_folder):
    for bus in buses:
        print bus
        if str(bus) == '186' :
            continue
        d = []
        sql = "select distinct trip_id from trips where diraction = {0} and route_id in (select route_id from routes where route_short_name = '{1}')".format(diraction,bus)
        trip_ids = db.First(db.Query(sql))

        if len(trip_ids) == 0:
            continue

        for trip_id in trip_ids:
            #print trip_id
            stopList = trips_stops[trip_id][0]

            oldTuple = get_list_for_marge(d,stopList) # is there any list we can marge stopList to it ?
            
            if oldTuple != None: # lets marge
                d.remove(oldTuple)
                trips = oldTuple[0] + [trip_id]
                if has_new(oldTuple[1],stopList): # is there any new stops in stopList
                    new_list = two_lists_new(oldTuple[1],stopList)
                else: # relax no marge on this list
                    new_list = oldTuple[1] 
                fnew = (trips, new_list)
            else: 
                fnew = ([trip_id],stopList)

            # add the new list 
            d.append(fnew)
        res = save_to_files(bus,d,diraction,target_folder)
        update_DB(res[0], res[1])

def has_new(l1,l2):
    """
        checks if list2 contints items thart are not in list1

        return True on the first new item
        return False in the end
    """
    for item in l2:
        if item not in l1:
            return True
    return False

def get_list_for_marge(d,l):
    """ search in l for a list that have same stop_ids like list d
    if there is (only one stop_id is required) ther it return the list
    else return None
    """
    for r in d:
        a = set(r[1]).intersection(set(l))
        if len(a) > 0:
            return r
    return None

def two_lists(l1, l2):
    reverse_flag =(l1[-1] != l2[-1])
    if reverse_flag:
        l1.reverse()
        l2.reverse()
    l3 = []
    flag = True
    while (flag):
        a1 = try_pop(l1)
        a2 = try_pop(l2)
        if a1 == None or a2 == None:
            flag = False
            break
        if a1 == a2:
            l3.append(a1)
        else:
            a3 = get_last(l3)
            if calc_dis(a3,a1) < calc_dis(a3,a2):
                l3.append(a1)
                l2.insert(0,a2)
            else:
                l3.append(a2)
                l1.insert(0,a1)
    if reverse_flag:
        if len(l1) > 0:
            l3 = l3 + l1
        l3.reverse()
    return l3

def two_lists_new(l1, l2):
    l3 = []
    p = get_first(l2,l1) # gets the first point in l2 that match l1
    if p == l1[0]:
        if p == l2[0]:
            pp = get_last_point(l2,l1)
            l3 = l3 + l2 + l1[l1.index(pp):]
        else:
            l3 = l3 + l2[:l2.index(p)] + l1
        res = two_lists(l3, l2)
    else:
        l3 = l3 +l2[:l2.index(p)] + l1[:l1.index(p)] + l2[l2.index(p):]
        res = two_lists(l3, l1)

    res.reverse()
    return res
    
def get_last_point(f,s):
    for i in f[::-1]:
        if i in s:
            return i
    return None

def get_first(f,s):
    for i in f:
        if i in s:
            return i
    return None

def try_pop(l):
    try:
        return l.pop()
    except:
        return None

def get_last(l):
    try:
        return l[-1]
    except:
        return 0

def calc_dis(p1,p2):
    if p1 == 0:
        p1 = (33.08924,35.10807)
        return(p1,stops[p2])
    return d(tuple(stops[p1][:2]),stops[p2][:2])

def save_to_files(bus_num,lists, diraction,target_folder):
    """
        save the lists of stops to files on the disk
        bus_num + diraction are used in name of the file

        return a list of tuples: (file name, trip id)
        the list contints all the trip_ids that were save with they file_name
    """
    res = []
    i = 0
    files_last_station = []
    for item in lists:
        key,value = item
        lines = []
        for stop_id in value:
            lines.append(','.join((stop_id, stops[stop_id][2],stops[stop_id][3])))
        file_name = '{0}_{1}_{2}'.format(bus_num,diraction,i)
        f = open(path.join(target_folder,file_name),'w')
        f.writelines('\n'.join(lines))
        f.close()
        i = i+1
        res.append((file_name, key))
        files_last_station.append( (file_name, stops[value[-1]][2] + ',' + stops[value[-1]][3]))
    return res, files_last_station

def update_DB(trips_files, files_last_station):
    l = []
    for r in trips_files:
        for trip_id in r[1]:
            l.append((trip_id,r[0],trips_stops[trip_id][1]))
    db.insert('trips_stops',l)

    l = []
    for r in files_last_station:
        l.append((r[0],r[1]))
    db.insert('files_last_station',l)

if __name__  == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('--db')
    parser.add_option('--rwe')
    parser.add_option('--target')
    (options, args) = parser.parse_args()
    db_path = options.db
    rwe = options.rwe
    target = options.target
else:
    db_path = 'tranz.sqlite'
    rwe = './rwe/'
    target = './new/'

print 'start'
db.init(db_path)
stops = set_stops(rwe)
trips_stops,b = set_trip_stops(rwe)
buses = db.First(db.Query('select distinct route_short_name from routes '))
run(0,target)
run(1,target)
db.close()
