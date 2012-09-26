import db
import time
from geopy import distance

distance.VincentyDistance.ELLIPOSID = 'WGS-84'
d = distance.distance

def find_old(lat,lon, acc):
    acc = int(float(acc))
    stime = time.time()
    sql = 'select * from distinct_new_shapes'
    #sql = 'select * from new_shape'
    l = db.Query(sql)
    print 'findTrips'
    res = set()
    for row in l:
        dis = d((lat,lon),(row[0],row[1])).meters
        if dis <= acc:
            print 'o'
            dis = d((lat,lon),(row[2],row[3])).meters
            if dis <= acc:
                print 'k'
                if type(row[4]) == type(1):
                    res.add(row[4])
                else:
                    for shape in row[4].split(';'):
                        res.add(int(shape))
    print time.time()-stime
    print len(res)
    return db.get_trips_ids('shape_id',res)

s1 = set()
def find(lat, lon, acc, trips_ids):
    acc = int(float(acc))
    s = "'" + "','".join(trips_ids) + "'"
    l = db.Query('select trip_id,t.shape_id,stops_ids from trips as t,shapes_to_stops as s where t.shape_id = s.shape_id and trip_id in ({0})'.format(s))
    stops_ids = [x[2] for x in l]
    for row in stops_ids:
        a = row.split(';')
        for r in a:
            s1.add(int(r))
    sql = 'select * from stops_ids where id in {0}'.format(tuple(s1))
    stops = db.Query(sql)
    
    stops_id_first = [(x[4],(x[0],x[1],x[2],x[3])) for x in stops]
    d_stops = dict(stops_id_first)

    res = []
    for row in l:
        for i in str(row[2]).split(';'):
            if d_stops[int(i)] == True:
                res.append(row[0])
                break;
            elif d_stops[int(i)] == False:
                pass
            else:
                r = calc(lat, lon, acc, d_stops[int(i)])
                if r == True:
                    res.append(row[0])
                    d_stops[int(i)] = True
                    break;
                else:
                    d_stops[int(i)] = False
    return res

def find_first(lat, lon, acc, trips_ids):
    acc = int(float(acc))
    s = "'" + "','".join(trips_ids) + "'"
    l = db.Query('select trip_id,t.shape_id,stops_ids from trips as t,shapes_to_stops as s where t.shape_id = s.shape_id and trip_id in ({0})'.format(s))
    stops_ids = [x[2] for x in l]
    for row in stops_ids:
        a = row.split(';')
        for r in a:
            s1.add(int(r))
    sql = 'select * from stops_ids where id in {0}'.format(tuple(s1))
    stops = db.Query(sql)
    
    stops_id_first = [(x[4],(x[0],x[1],x[2],x[3])) for x in stops]
    d_stops = dict(stops_id_first)

    for row in l:
        for i in str(row[2]).split(';'):
            r = calc(lat, lon, acc, d_stops[int(i)])
            if r == True:
                return True
    return False

def calc(lat,lon,acc, point):
    dis = d((lat,lon),(point[0],point[1])).meters
    if dis <= acc:
        dis = d((lat,lon),(point[2],point[3])).meters
        if dis <= acc:
            return True
    return False

