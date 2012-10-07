import db
import model

def get_model(bus_num):
    sql = 'select * from bus_root where bus_num={0}'.format(bus_num)
    l = db.Query(sql)
    b = model.bus_root(bus_num)
    for row in l:
        b.add(row[1],row[2],row[3],row[4],row[5],row[6],row[7])
    return b

def create_user_data(lat,lon,acc,hour,day):
    return model.user_data(lat,lon,acc,hour,day)

def test():
    a = get_model(921)
    u = create_user_data('32.308789','34.901497','200.0','10:00:00','sunday')
    return a,u

