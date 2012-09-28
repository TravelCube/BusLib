import sqlite3
from model import *

conn = sqlite3.connect('/home/omer/tranz/gith/Bus/DB/tranz.sqlite')
conn.text_factory = str

def Query(sql):
    c = conn.cursor()
    c.execute(sql)
    l = c.fetchall()
    c.close()
    return l

def query_open(sql):
    c = conn.cursor()
    c.execute(sql)
    return c

def First(l):
     return [r[0] for r in l]

def get_trips_ids(col,l):
    sql = 'select distinct trip_id from trips where {0} in {1}'.format(col,tuple(l))
    return First(Query(sql))

def create_table(name, *args):
    print args
    c = conn.cursor()
    sql = 'create table {0} ({1})'.format(name,'{0}')
    l = ''
    for arg in args:
	print arg
        l = l + arg[0] + ' ' + arg[1] + ','
    l = l[:-1]
    print sql,l
    sql = sql.format(l)
    print sql
    c.execute(sql)
    conn.commit()
    c.close()
    
def insert(table,l):
    c = conn.cursor()
    n = len(l[0])
    sql = 'insert into {0} values ({1})'.format(table, ('?,'* n)[:-1])
    c.executemany(sql, l)
    conn.commit()
    c.close()

def update(sql):
    c = conn.cursor()
    c.execute(sql)
    conn.commit
    c.close()

def get_data(bus_num):
    sql = 'select routes.agency_id,t.diraction,ts.file_name,t.trip_id,t.service_id,rides.start_time, t.shape_id from routes join trips as t on t.route_id = routes.route_id join trips_stops as ts on t.trip_id=ts.trip_id join rides on t.trip_id = rides.trip_id where bus_num={0}'.format(bus_num)
    l = Query(sql)
    b = bus_root(bus_num)
    for row in l:
        b.add(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
    return b

def get_all_data():
    buses = {}
    sql = 'select routes.bus_num, routes.agency_id,t.diraction,ts.file_name,t.trip_id,t.service_id,rides.start_time,t.shape_id from routes join trips as t on t.route_id = routes.route_id join trips_stops as ts on t.trip_id=ts.trip_id join rides on t.trip_id = rides.trip_id '
    l = Query(sql)
    print 'start'
    print l[0]
    for row in l:
        if row[0] not in buses:
            buses[row[0]] = bus_root(row[0])
        buses[row[0]].add(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
    return buses

import pickle
#f = open('./helpers/buses.pickle' ,'r')
#buses = pickle.load(f)
#if buses == None:
#    print 'error'
#buses = get_all_data()
#pickle.dump(buses,f)
#f.close()
            
def get_bus(bus_num):
    return get_data(bus_num)
    #return buses[bus_num]
