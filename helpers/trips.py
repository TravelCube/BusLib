import db

def get_routes(trips_ids):
    s = "'" + "','".join(trips_ids) + "'"
    sql = 'select route_id,trip_id from trips where trip_id in ({0})'.format(s)
    l = db.Query(sql)
    return l
