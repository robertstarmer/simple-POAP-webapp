Simple PoAP Web App
===================

This is a simple app that allows a PoAP capable device to update a database with it's base config info, and retrieve a config file based on a simple templated file.

Copy the files to a web user accessible location (/opt/cisco would work)
Add:
 WSGIScriptAlias /cisco /opt/cisco/application.wsgi

To the appropriate VirtualHost section for Apache (assuming you're running Apache)
  e.g. in /etc/apache2/sites-available/default between the <VirtualHost *:80> </VirtualHost> markers.

If there's not one already, you'll also need to create a MYSQL database, and update the /opt/cisco/application.wsgi file with the appropriate user/password to access the database.

