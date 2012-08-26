#!/usr/bin/python
#
#This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 United States License. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/us/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
#
# (CC) BY SA - Robert Starmer, Cisco Systems, Inc. August, 2012
# 
# References:
# WSGI: http://library.linode.com/web-servers/apache/mod-wsgi/fedora-14
# MYSQL: http://www.kitebird.com/articles/pydbapi.html
#
# Useage Example:
# curl -d hostname=01-e3-alpha -d macaddr=00:01:DE:AD:BE:AF -d model=nexus3064  http://192.168.25.24/cisco
# Should return:
# ConfigFile: 01-e3-alpha.cfg
# MD5File: 01-e3-alpha.md5
#
import os
import MySQLdb as mdb
import sys
from urlparse import parse_qs, parse_qsl

sys.path.append('/opt/cisco')

os.environ['PYTHON_EGG_CACHE'] = '/opt/cisco/.python-egg'

def application(environ, start_response):

    con = None

    try:
	con = mdb.connect('localhost','cisco','Cisco123','cisco');
	cur = con.cursor()
    except mdb.Error, e:
    	print "Error %d: %s" % (e.args[0],e.args[1])
    	sys.exit(1)

	
    try:
	request_body_size = int(environ.get('CONTENT_LENGTH',0))
    except (ValueError):
        request_body_size = 0
    
    if environ['REQUEST_METHOD'] == 'POST':
    	request_body = environ['wsgi.input'].read(request_body_size)
    	d = parse_qs(request_body)
	
	hn = d.get('hostname')[0]
	ma = d.get('macaddr')[0]
	mo = d.get('model')[0]

	cur.execute('INSERT INTO cisco(hostname, macaddr, model) VALUES("%s", "%s", "%s")' % (hn,ma,mo))
	row = cur.rowcount

	cur.close()
	con.commit()
	con.close()

	
        start_response('200 OK', [('content-type', 'text/html')])
	return ['ConfigFile: ', hn, '.cfg\n', 'MD5File: ', hn, '.md5\n', 'Inserted into db: ', str(row), '\n']

    else:
        start_response('200 OK', [('content-type', 'text/html')])
        return ["""
	<form method="POST">
	<p>Hostname: <input type="text" name="hostname" value="rr-ra-a">
	<p>MacAddr: <input type="text" name="macaddr" val="00:00:00:00:00:00">
	<p>Model: <input type="text" name="model" value="Nexus-3064">
	<p><input type="submit"></form>

"""]

