#!/usr/bin/python
import MySQLdb
import requests
import json
from datetime import datetime
import time

num = 10

src = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","ebdb")
url = 'http://localhost:8001/api/planttimeseries'

sql = "select a.*,b.HPOA_DIFF as hpoa_diff from PlantTimeSeries a, PVARrayTimeSeries b where a.fkPlant=b.fkPlant and a.Timestamp=b.Timestamp and a.fkPlant<=%s"

cursor = src.cursor()

cursor.execute(sql % (num))

results = cursor.fetchall()

print( "results has %d rows" % (len(results)))

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
			"recordstatus":row[1]
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
