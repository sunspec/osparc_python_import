#!/usr/bin/python
import MySQLdb
import requests
import json
from datetime import datetime
import time
import sys

try:
	num = sys.argv[1]
	host = sys.argv[2]
	user = sys.argv[3]
	pwrd = sys.argv[4]
except:
	print "usage: python import_plants.py <number of plants> <db host> <db user> <db pw>"
	quit()

print "importing timeseries from %s plants from host %s" %(num,host)

src = MySQLdb.connect(host,user,pwrd,"ebdb")
url = 'http://localhost:8001/api/v1/planttimeseries'

sql = "select a.*,b.HPOA_DIFF as hpoa_diff,c.PlantUUID as uuid from PlantTimeSeries a, PVArrayTimeSeries b, Plants c where a.fkPlant=b.fkPlant and a.fkPlant=c.id and a.Timestamp=b.Timestamp and a.fkPlant<=%s"

cursor = src.cursor()

cursor.execute(sql % (num))

results = cursor.fetchall()

print( "retrieved %d rows from ebdb" % (len(results)))

try:
	for row in results:

		jsonStr = json.dumps(
		{ 
			"timestamp": row[3].isoformat(),
			"sampleinterval": row[4],
			"WH_DIFF": row[6],
			"GHI_DIFF": row[8],
			"TMPAMB_AVG": row[9],
			"HPOA_DIFF": row[45],
			"recordstatus":row[1],
			"plantUUID":row[46]
		},sort_keys=True,indent=4)

		response = requests.post(url,headers={"Content-Type":"application/json"},data=jsonStr)
		if response.status_code == 201:
			print "added entry plant %s timestamp %s" % (row[2],row[3].isoformat())
		else:
			print "failed to add entry plant %s timestamp %s. status %s: %s" % (row[2],row[3].isoformat(),response.status_code,response.text)

		time.sleep(.01)
except:
	print "ERROR"

src.close()
