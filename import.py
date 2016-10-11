#!/usr/bin/python
import MySQLdb
import requests
import json
from datetime import datetime
import time

src = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","ebdb")
dst = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","osparc")
url = 'http://localhost:8000/api/plants'

plantSql = "select * from Plants where id>10 and id<=100"
pvArraySql = "select TrackerType,Tilt,Azimuth from PVArrays where fkPlant=%s"

cursor = src.cursor()

cursor.execute(plantSql)

results = cursor.fetchall()

try:
	print( "results has %d rows" % (len(results)))
	for row in results:
		recordStatus = row[2]
		versionCreationTime = row[3]
		versionID = row[4]
		plantUUID = row[5]
		accountID = row[6]
		name = row[7]
		description = row[8]
		activationDate = row[9]
		postalCode = row[10]
		state = row[11]
		county = row[12]
		city = row[13]
		latitude = row[14]
		longitude = row[15]
		timeZone = row[16]
		weatherSource = row[20]
		DCRating = row[24]
		derate = row[25]
		solarAnywhereSite = row[27]

		sql = pvArraySql % (row[0])
		pvaCursor = src.cursor()
		pvaCursor.execute(sql)
		pvArray = pvaCursor.fetchone()
		trackerType = pvArray[0]
		tilt = pvArray[1]
		azimuth = pvArray[2]
		print "adding %s" % (name)


		jsonStr = json.dumps(
			{ "recordStatus":recordStatus,
			  "versionCreationTime":versionCreationTime.isoformat(),
			  "versionID":versionID,
			  "plantUUID":plantUUID,
			  "accountID":accountID,
			  "name":name,
			  "description":description,
			  "activationDate":activationDate.isoformat(),
			  "postalCode":postalCode,
			  "state":state,
			  "county":county,
			  "city":city,
			  "latitude":latitude,
			  "longitude":longitude,
			  "timeZone":timeZone,
			  "weatherSource":weatherSource,
			  "DCRating":DCRating,
			  "derate":derate,
			  "solarAnywhereSite":solarAnywhereSite,
			  "trackerType":trackerType,
			  "tilt":tilt,
			  "azimuth":azimuth
			},sort_keys=True,indent=4)

		response = requests.post(url,headers={"Content-Type":"application/json"},data=jsonStr)
		if response.status_code == 201:
			print "added %s (activated %s)" % (name,activationDate.isoformat())
		else:
			print "status: "+response.status_code

		time.sleep(.1)
except:
	print "ERROR"

src.close()
