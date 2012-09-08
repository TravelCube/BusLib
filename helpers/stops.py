import db

def get_stops_lat_lon(ids):
    sql = 'select id,lat,lon from stops where id in {0}'.format(tuple(ids))
    print sql
    l = db.Query(sql)
    res = {}
    for r in l:
        res[r[0]] = (r[1],r[2])
    return res 
