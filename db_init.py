import os
import MySQLdb as mdb
import sys
sys.path.append('/opt/cisco')

con = None

try:
  con = mdb.connect('localhost','cisco','Cisco123','cisco');
  cur = con.cursor()
  cur.execute("SELECT VERSION()")
  row = cur.fetchone()
except mdb.Error, e:
  print "Error %d: %s" % (e.args[0],e.args[1])
  sys.exit(1)

cur.execute("DROP TABLE IF EXISTS cisco")
cur.execute("""
  CREATE TABLE cisco
  (
	Id INT PRIMARY KEY AUTO_INCREMENT,
	hostname	CHAR(128),
	macaddr CHAR(18),
	model   CHAR(20),
	env	CHAR(20),
	row	CHAR(10),
	rack	CHAR(10),
	vendor	CHAR(20),
	lbip	CHAR(20),
	intvlanip	CHAR(20),
	ul1ip	CHAR(20),
	ul2ip	CHAR(20),
	nh1ip	CHAR(20),
	nh2ip	CHAR(20)
  )
""")

cur.close()
con.close()
