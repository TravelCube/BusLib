import db

def find(day):
    sql = 'select service_id from calendar where {0} = 1'.format(day)
    return db.get_trips_ids('service_id',db.First(db.Query(sql)))

def find(day,trip_ids):
    s = "'" + "','".join(trip_ids) + "'"
    sql = 'select trips.trip_id from trips join calendar as c on trips.service_id = c.service_id where c.{0} = 1 and trips.trip_id in ({1})'.format(day,s)
    return db.First(db.Query(sql))
