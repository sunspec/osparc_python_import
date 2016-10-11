#!/usr/bin/python
import MySQLdb
import requests
import json
from datetime import datetime
import time

src = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","ebdb")
url = 'http://localhost:8001/api/planttimeseries'

sql = "select a.*,b.HPOA_DIFF as hpoa_diff from PlantTimeSeries a, PVARrayTimeSeries b where a.fkPlant=b.fkPlant and a.Timestamp=b.Timestamp and a.fkPlant>43 and a.fkPlant<=100"

cursor = src.cursor()

cursor.execute(sql)

results = cursor.fetchall()

try:
	for row in results:

		jsonStr = json.dumps(
		{ 
			"timeStamp": row[3].isoformat(),
			"sampleInterval": row[4],
			"WH_DIFF": row[6],
			"GHI_DIFF": row[8],
			"TMPAMB_AVG": row[9],
			"HPOA_DIFF": row[45],
			"plant": row[2],
			"recordStatus":row[1]
		},sort_keys=True,indent=4)

		response = requests.post(url,headers={"Content-Type":"application/json"},data=jsonStr)
		if response.status_code == 201:
			print "added %s (timestamp %s)" % (row[2],row[3].isoformat())
		else:
			print "status: "+response.status_code

		time.sleep(.05)
except:
	print "ERROR"

src.close()
