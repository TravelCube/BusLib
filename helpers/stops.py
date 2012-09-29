import db

def get_stops_lat_lon(ids):
    sql = 'select id,lat,lon from stops where id in {0}'.format(tuple(ids))
    print sql
    l = db.Query(sql)
    res = {}
    for r in l:
        res[r[0]] = (r[1],r[2])
    return res 

def get_stop_files_last_station(file_names):
    sql = 'select file_name,last from stops_files_stations where file_name in {0}'.format(tuple(file_names))
    print sql
    return db.Query(sql)
