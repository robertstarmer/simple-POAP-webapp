#!/usr/bin/python
import sys
import os
import MySQLdb as mdb
from mako.template import Template

sys.path.append('/opt/cisco')

#import hashlib
#[(fname, hashlib.md5(open(fname, 'r').read()).digest()) for fname in fnamelst]

con = None

try:
	con = mdb.connect('localhost','cisco','Cisco123','cisco');
except mdb.Error, e:
    	print "Error %d: %s" % (e.args[0],e.args[1])
    	sys.exit(1)

cur = con.cursor()
cur.execute ("DROP TABLE IF EXISTS cisco")
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
cur.execute("""
  INSERT INTO cisco (hostname, macaddr, model, env, row, rack, vendor, lbip, intvlanip, ul1ip, ul2ip, nh1ip, nh2ip)
  VALUES
    ('aa-bb-cc', '00:11:22:33:44:cc', 'Nexus-3064', 'ITS', '1','1','cisco','17.1.1.100','17.10.1.1','17.100.1.250','17.100.1.251','17.100.1.252/24','17.100.1.253/24'),
    ('aa-bb-dd', '00:11:22:33:44:dd', 'Nexus-3064', 'ITS', '1','1','cisco','17.1.1.100','17.10.1.2','17.100.1.250','17.100.1.251','17.100.1.252/24','17.100.1.253/24'),
    ('aa-bb-ee', '00:11:22:33:44:ee', 'Nexus-3064', 'ITS', '1','2','cisco','17.1.1.101','17.10.1.3','17.100.2.250','17.100.2.251','17.100.2.252/24','17.100.2.253/24'),
    ('aa-bb-ff', '00:11:22:33:44:ff', 'Nexus-3064', 'ITS', '1','2','cisco','17.1.1.101','17.10.1.4','17.100.2.250','17.100.2.251','17.100.2.252/24','17.100.2.253/24')
  """)

row = cur.rowcount

print "Number of rows inserted: %d" % row

cur.close()
con.commit()

config_tmpl = Template(filename='templates/config.tmpl')
cur = con.cursor()
cur.execute("""SELECT * FROM cisco""")
results = cur.fetchall()

for row in results:
  hostname = row[1]
  vl10ip = row[8]
  ul1ip = row[9]
  ul2ip = row[11]
  nh1ip = row[12]
  nh2ip = row[13]
  print config_tmpl.render(hostname=hostname, vl10ip=vl10ip, ul1ip=ul1ip, ul2ip=ul2ip, nh1ip=nh1ip, nh2ip=nh2ip)

con.close()

