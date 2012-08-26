import os
import MySQLdb as mdb
import sys
from urlparse import parse_qs, parse_qsl
#from jinja2 import Environment, PackageLoader
#env = Environment(loader=PackageLoader('application', 'templates'))
#from jinja2 import Template
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
	con.close()

	
        start_response('200 OK', [('content-type', 'text/html')])
	return ['ConfigFile: ', hn, '.cfg\n', 'MD5File: ', hn, '.md5\n']

    else:
        start_response('200 OK', [('content-type', 'text/html')])
        return ["""
	<form method="POST">
	<p>Hostname: <input type="text" name="hostname" value="rr-ra-a">
	<p>MacAddr: <input type="text" name="macaddr" val="00:00:00:00:00:00">
	<p>Model: <input type="text" name="model" value="Nexus-3064">
	<p><input type="submit"></form>

"""]

