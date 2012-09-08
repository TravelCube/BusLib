import db
from datetime import datetime

def find(hour,trips_ids):
    hour = datetime.strptime(hour,'%H:%M:%S')
    s = "'" + "','".join(trips_ids) + "'"
    sql = 'select * from rides where trip_id in ({0})'.format(s)
    l = db.Query(sql)
    res = []
    for row in l:
        t = datetime.strptime(row[1],'%Y-%m-%d %H:%M:%S')
        if hour > t:
            res.append(row[0])
    return res

def get_stop_files(trips_ids):
    s = "'" + "','".join(trips_ids) + "'"
    sql = 'select distinct file_name from rides where trip_id in ({0})'.format(s)
    l = db.First(db.Query(sql))
    return l
