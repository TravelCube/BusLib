import db
import stops
import model
import memcache
#from celery import group
#from tasks import check

mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def get_model(bus_num):
    obj = mc.get(bus_num)
    if obj != None:
        print 'ok'
        return obj

    sql = 'select * from bus_root where bus_num={0}'.format(bus_num)
    l = db.Query(sql)
    b = model.bus_root(bus_num)
    for row in l:
        b.add(row[1],row[2],row[3],row[4],row[5],row[6])
    mc.set(bus_num,b)
    return b

def create_user_data(lat,lon,acc,hour,day):
    return model.user_data(lat,lon,acc,hour,day)

def test(bus):
    a = get_model(bus)
    u = create_user_data('32.311727','34.902055','700.0','12:00:00','sunday')
    print a,u
    return get_file_names_from_bus_num(bus,'32.311727','34.902055','700.0','15:00:00','sunday')

def get_file_names_from_bus_num(bus_num, lat, lon, acc, hour, day):
    m = get_model(bus_num)
    res =  m.find_file_names(create_user_data(lat, lon, acc, hour, day))
    if res == None:
        print 'error!!!!'
    print res
    if res[1] == None:
        res = [res[0]]
    return _get_files_first_stop(res)

def _get_files_first_stop(file_names):
        """ find the stops files and the last station name for the trip ids

            return distinct list of stop_file, last station
        """
        l = stops.get_stop_files_last_station(file_names)
        return l

def get_parallel(bus_num, lat, lon, acc, hour, day):
    userd = create_user_data(lat, lon, acc, hour, day)
    m = get_model(bus_num)
    if len(m.agencies) == 1:
        agency = m.agencies.values()[0]
    g = group(check.s(t,userd) for t in m.agencies.values())
    res = g.apply_async()
    for r in res.iterate():
        if r[0] != False:
            res.revoke()
            agency, false_list = r

    file_name0, false_list = agency.diractions[0].find_file_name_macth(userd, false_list)
    file_name1, false_list = agency.diractions[1].find_file_name_macth(userd, false_list)
    return (file_name0, file_name1)
