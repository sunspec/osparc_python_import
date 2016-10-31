#!/usr/bin/python
import MySQLdb
import requests
import json
from datetime import datetime
import time
import sys

num = sys.argv[1]
print ("importing timeseries from %s plants" %(num))


src = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","ebdb")
url = 'http://localhost:8001/api/planttimeseries'

sql = "select a.*,b.HPOA_DIFF as hpoa_diff,c.PlantUUID as uuid from PlantTimeSeries a, PVARrayTimeSeries b, Plants c where a.fkPlant=b.fkPlant and a.fkPlant=c.id and a.Timestamp=b.Timestamp and a.fkPlant<=%s"

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
			"plant": row[2],
			"recordstatus":row[1],
			"plantUUID":row[46]
		},sort_keys=True,indent=4)

		print jsonStr

		response = requests.post(url,headers={"Content-Type":"application/json"},data=jsonStr)
		if response.status_code == 201:
			print "added entry plant %s timestamp %s" % (row[2],row[3].isoformat())
		else:
			print "failed to add entry plant %s timestamp %s. status %s: %s" % (row[2],row[3].isoformat(),response.status_code,response.text)

		time.sleep(.01)
except:
	print "ERROR"

src.close()
