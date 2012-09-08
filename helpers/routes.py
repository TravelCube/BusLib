import db

def find(bus_line):
    sql = 'select route_id from routes where bus_num = {0}'.format(bus_line)
    ids = db.First(db.Query(sql))
    return db.get_trips_ids('route_id',ids)

def get_long_names(routes_ids):
    sql = 'select route_id,text from routes where route_id in {0}'.format(tuple(routes_ids))
    res = db.Query(sql)
    return res
