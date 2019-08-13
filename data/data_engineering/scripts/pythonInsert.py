import pymysql
import json
connection = pymysql.connect(host='csi420-01-vm9.ucd.ie',
                             user='niamh',
                             password='comp47360jnnd',
                             db='website',
                             cursorclass=pymysql.cursors.DictCursor)
with open('frontEndBusInfo.json') as json_file:  
        data = json.load(json_file)

try:
    with connection.cursor() as cursor:
        for stop in data:
            for route in data[stop]['routes'][0]:
                sql = "INSERT INTO routes_per_stop (route_id, stop_id) VALUES (%s, %s)"
                cursor.execute(sql, (route, stop))
            connection.commit()

finally:
    connection.close()
