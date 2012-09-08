import db

def find(day):
    sql = 'select service_id from calendar where {0} = 1'.format(day)
    return db.get_trips_ids('service_id',db.First(db.Query(sql)))
