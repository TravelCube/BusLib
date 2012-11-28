import db
from os import path

def set_shapes(rwe_data_path):
    """ return a dict that hold data from stops.txt
        dict[stop_id] = (lat, lon, name, desc)
    """
    f = open(path.join(rwe_data_path, 'shapes.txt'), 'r')
    shapes = []
    f.next()
    for row in f:
        row = row.split(',')
        shapes.append(row)
    return shapes


def run(shapes):
    rer = lambda x: (x[2],x[3],x[0],x[1])
    lines = {}
    for i in range(0,len(shapes)-1):
        start = shapes[i]
        end = shapes[i+1]
        if int(start[3]) == int(end[3])-1: # check the sequence
            line = (start[1],start[2],end[1],end[2])
            if line not in lines and rer(line) not in lines:
                lines[line] = []
            if line in lines:
                lines[line].append(start[0])
            else:
                lines[rer(line)].append(start[0])

    lines_table = []
    shapes_to_lines = []
    i = 1
    for a,value in lines.iteritems():
        lines_table.append((a[0],a[1],a[2],a[3],i))
        for shape in value:
            shapes_to_lines.append((shape,i))
        i = i+1

    db.insert('lines',lines_table)
    db.insert('shapes_to_lines',shapes_to_lines)

if __name__  == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('--db')
    parser.add_option('--rwe')
    (options, args) = parser.parse_args()
    db_path = options.db
    rwe = options.rwe
else:
    db_path = 'tranz.sqlite'
    rwe = './rwe/'

print 'start'
db.init(db_path)

run(set_shapes(rwe))

db.close()
