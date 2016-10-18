#!/usr/bin/python
import MySQLdb
import requests
import json
from datetime import datetime
import time

num = 1
db = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","osparc")

plantSql = "select * from Plants where id<=%d"
pvArraySql = "select TrackerType,Tilt,Azimuth from PVArrays where fkPlant=%s"

cursor = src.cursor()

cursor.execute(plantSql % (num))

results = cursor.fetchall()

try:
	print( "results has %d rows" % (len(results)))

	for row in results:

		if row.dcrating is not null:
			


		response = requests.post(url,headers={"Content-Type":"application/json"},data=jsonStr)
		if response.status_code == 201:
			print "added %s (activated %s)" % (name,activationDate.isoformat())
		else:
			print "status: "+response.status_code

		time.sleep(.01)
except:
	print "ERROR"

src.close()
