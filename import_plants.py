#!/usr/bin/python
import MySQLdb
import requests
import json
from datetime import datetime
import time
import sys

num = sys.argv[1]

print ("importing %s plants" %(num))

src = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","ebdb")
url = 'http://localhost:8001/api/plants'

plantSql = "select * from Plants where id<=%s"
pvArraySql = "select TrackerType,Tilt,Azimuth from PVArrays where fkPlant=%s"

cursor = src.cursor()

cursor.execute(plantSql % (num))

results = cursor.fetchall()

try:
	print( "retrieved %d row from ebdb" % (len(results)))

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

		jsonStr = json.dumps(
			{ "recordstatus":recordStatus,
			  "versioncreationtime":versionCreationTime.isoformat(),
			  "versionid":versionID,
			  "plantuuid":plantUUID,
			  "accountid":accountID,
			  "name":name,
			  "description":description,
			  "activationdate":activationDate.isoformat(),
			  "postalcode":postalCode,
			  "state":state,
			  "county":county,
			  "city":city,
			  "latitude":latitude,
			  "longitude":longitude,
			  "timezone":timeZone,
			  "weathersource":weatherSource,
			  "dcrating":DCRating,
			  "derate":derate,
			  "solaranywheresite":solarAnywhereSite,
			  "trackertype":trackerType,
			  "tilt":tilt,
			  "azimuth":azimuth
			},sort_keys=True,indent=4)

		response = requests.post(url,headers={"Content-Type":"application/json"},data=jsonStr)
		if response.status_code == 201:
			print "added %s (activated %s)" % (name,activationDate.isoformat())
		else:
			print "failed to add plant %s. status %s: %s" % (name,response.status_code,response.text)

		# time.sleep(.01)
except:
	print "ERROR"

src.close()
