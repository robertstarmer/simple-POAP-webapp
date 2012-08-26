#!/usr/bin/python
import os
import MySQLdb as mdb

con = None

try:
	con = mdb.connect('localhost','cisco','Cisco123','cisco');
except mdb.Error, e:
    	print "Error %d: %s" % (e.args[0],e.args[1])
    	sys.exit(1)

cur = con.cursor()
cur.execute ("DROP TABLE IF EXISTS cisco")
cur.execute ("""
  CREATE TABLE cisco
  (
    hostname  CHAR(40),
    macaddr   CHAR(40),
    model     CHAR(40)
  )
  """)

cur.execute("""
  INSERT INTO cisco (hostname, macaddr, model)
  VALUES
    ('aa-bb-cc', '00:11:22:33:44:55', 'Nexus-3064'),
    ('dd-ee-ff', 'aa:11:22:33:44:55', 'Nexus-3064')
  """)

row = cur.rowcount

print "Number of rows inserted: %d" % row

hn = 'aa-bb-cc-host'
ma = '00:11:22:11:00:11'
mo = 'Nexus-3064'

cur.execute('INSERT INTO cisco(hostname, macaddr, model) VALUES("%s", "%s", "%s")' % (hn,ma,mo))

row = cur.rowcount

print "Number of rows inserted: %d" % row

cur.close()
con.commit()
con.close()

