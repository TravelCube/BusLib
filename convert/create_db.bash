#!/bin/bash

#mkdir ./rwe
#wget -O ./rwe/rwe.zip ftp://199.203.58.18/israel-public-transportation.zip 
#unzip -q -d ./rwe ./rwe/rwe.zip


sqlite3 -batch tranz.sqlite <<EOF
create table trips (route_id int, service_id int, trip_id text, diraction int, shape_id int);
.mode csv
.import ./rwe/trips.txt trips

create table routes (route_id int, agency_id int, route_short_name text, route_long_name text, route_desc text, route_type int);
.import ./rwe/routes.txt routes

create table calendar (service_id int, sunday int, monday int, tuesday int, wednesday int, thursday int, friday int, saturday int, start_date text, end_date text);
.import ./rwe/calendar.txt calendar

create table trips_stops ( trip_id text, file_name text, start_time text);
create table files_last_station ( file_name text, last_station text);

create table lines ( s_lat float, s_lon float, e_lat float, e_lon float, line_id int);
create table shapes_to_lines ( shape_id text, line_id int);
EOF

mkdir ./stops_files

python ./stops_files_marge.py --db tranz.sqlite --rwe ./rwe --target ./stops_files

python ./pross_shape.py --db tranz.sqlite --rwe ./rwe

sqlite3 -batch tranz.sqlite << EOF
create table bus_root( bus_num text, agency_id int, diraction int, file_name text, shape_id text, service_id text, start_time text);

insert into bus_root
select route_short_name, agency_id, diraction, file_name, shape_id, service_id, min(start_time) from trips as t join trips_stops as s on t.trip_id = s.trip_id join routes as r on r.route_id = t.route_id group by file_name, shape_id, service_id;

drop table routes;
drop table trips_stops;
drop table trips;

VACUUM;

EOF

#rm -r ./rwe
