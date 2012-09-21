import db

def get_stops_lat_lon(ids):
    sql = 'select id,lat,lon from stops where id in {0}'.format(tuple(ids))
    print sql
    l = db.Query(sql)
    res = {}
    for r in l:
        res[r[0]] = (r[1],r[2])
    return res 

def get_stop_files_last_station(trip_ids):
    s = "'" + "','".join(trip_ids) + "'"
    sql = 'select file_name,last from stops_files_stations where file_name in (select distinct file_name from trips_stops where trip_id in ({0}))'.format(s)
    return db.Query(sql)
