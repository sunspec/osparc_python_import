#!/usr/bin/python
import MySQLdb
import requests
import json
from datetime import datetime

src = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","ebdb")
dst = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","osparc")
url = 'http://localhost:8000/api/plants'

plantSql = "select * from Plants where id>0 and id<=1"
pvArraySql = "select TrackerType,Tilt,Azimuth from PVArrays where fkPlant=%s"

cursor = src.cursor()

cursor.execute(plantSql)

results = cursor.fetchall()

try:
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
		print sql
		cursor.execute(sql)

		pvArray = cursor.fetchone()
		trackerType = pvArray[0]
		tilt = pvArray[1]
		azimuth = pvArray[2]
		print "tt= %s, tilt=%s, azimuth=%s" % (trackerType,tilt,azimuth)


		json = json.dumps(
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
		print json

		response = requests.post(url,headers={"Content-Type":"application/json"},data=json)
except:
	print "ERROR"

src.close()
