#!/usr/bin/python
import sys
import psycopg2
import psycopg2.extras
from Search import *

positive_terms = ['rocks', 'rules']
negative_terms = ['sucks']

username = 'srom_collector'
passwd = ''
hostname = 'localhost'
dbname = 'srom'

try:
	conn = psycopg2.connect(database=dbname, user=username, host=hostname, password=passwd)
except:
	print "Unable to connect to the database."
	exit(1)

# Build a set of search engines
curr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

curr.execute("""SELECT * FROM sites""")

search_list = []

for row in curr:
	if (row['class'] != 'Disabled'):
		search_object = getattr(sys.modules[__name__], row['class'])()
		search_object.configure(row)
		search_list.append(search_object)

# Get the search items
curr.execute("""SELECT * FROM terms""")
rows = curr.fetchall()

results = {}

# Search for each term set
for search in search_list:
	print "Searching with site ID " + str(search.getID())
	try:
		curr.execute("BEGIN;")
		for row in rows:
			positive = 0
			negative = 0
			queries = 0
			for item in row['items']:
				for term in positive_terms:
					positive = positive + int(search.getCounts('"' + item + ' ' + term + '"'))
					queries = queries + 1
				for term in negative_terms:
					negative = negative + int(search.getCounts('"' + item + ' ' + term + '"'))
					queries = queries + 1
			curr.execute("INSERT INTO results (updated, site_id, positive_count, negative_count, queries, name) VALUES (now(), %s, %s, %s, %s, %s)", (search.getID(), positive, negative, queries, row['name']))
		print "Commiting results for site ID " + str(search.getID())
		curr.execute("COMMIT;")	
	except:
		print "Error, search " + str(search.getID()) + " is having trouble."
		curr.execute("ABORT;")
		

conn.commit()
curr.close()
conn.close()
