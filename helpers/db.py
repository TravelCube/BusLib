import sqlite3

conn = sqlite3.connect('/home/omer/tranz/gith/Bus/DB/tranz.sqlite')
conn.text_factory = str

def Query(sql):
    c = conn.cursor()
    c.execute(sql)
    l = c.fetchall()
    c.close()
    return l

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
