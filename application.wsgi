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
	cur.execute("SELECT VERSION()")
	row = cur.fetchone()
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
        start_response('200 OK', [('content-type', 'text/html')])
        return ['Hostname: ', d.get('hostname')[0], '\n', 'Mac Addr: ', d.get('macaddr')[0], '\n', 'Model: ', d.get('model')[0], '\n', 'DB Version: ', row[0] ,'\n']
    else:
        start_response('200 OK', [('content-type', 'text/html')])
        return ['<form method="POST">Name: <input type="text" '
                'name="name"><input type="submit"></form>']
