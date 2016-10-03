#!/usr/bin/python
import MySQLdb

src = MySQLdb.connect("aa1mdgyhr3b9jaa.cfzeszoxdqzd.us-west-2.rds.amazonaws.com",
	"osparcdb","0sparcd6","ebdb")
dest = MySQLdb.connect("localhost","root","PythonMySQLoSPARC","osparc")

cursor = src.cursor()
cursor.execute("select version()")
data = cursor.fetchone()
print "Database version : %s " % data

db.close()

