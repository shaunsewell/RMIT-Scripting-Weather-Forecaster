#!/usr/bin/python

#!/usr/bin/env python

# from http://www.acmesystems.it/python_httpserver
# Python 2

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import os.path

import cgi
import routes
import urlparse

from dispatchToMethod import getController


# decide where input paths should be directed to
# import routes

PORT_NUMBER = 34567


# This class will handles any incoming request from
# the browser	
	
class myHandler(BaseHTTPRequestHandler):
	
	# Handler for the GET requests
	def do_GET(self):
		assetsDir = "assets"
		asset = False
		
		try:
			# Check the file extension required and
			# set the right mime type

			print self.path
			if self.path.endswith(".jpg"):
				mimetype = 'image/jpg'
				asset = True
				
			elif self.path.endswith(".gif"):
				mimetype = 'image/gif'
				asset = True
				
			elif self.path.endswith(".js"):
				mimetype = 'application/javascript'
				sendReply = True
				print "javascript!"
				asset = True
				
			elif self.path.endswith(".css"):
				mimetype = 'text/css'
				asset = True
				
			else:
				# strip trailing slash of the path if present
				self.path = self.path.rstrip('/')
				mimetype = 'text/html'

			self.send_response(200)
			self.send_header('Content-type', mimetype)

			self.end_headers()
			
			# should we send an asset, or should we generate a page?
			if asset == True:
				# Open the static file requested and send it
				# assets all live in an asset directory

				path = os.path.abspath(assetsDir + self.path)

				f = open(path)
				self.wfile.write(f.read())
				f.close()
			else:
				# a page!
				newURL, method = getController('GET', self.path)
				self.wfile.write(method())

			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Handler for the POST requests
	def do_POST(self):
		# check the URL requested in the incoming request
		# you can handle multiple URLs here
		
		# get all the interesting goodness from the incoming post
		form = cgi.FieldStorage(
			fp = self.rfile, 
			headers = self.headers,
			environ = {'REQUEST_METHOD':'POST',
	                   'CONTENT_TYPE'  :'Content-Type',
					  },
			keep_blank_values = True
			)


		# move the cgi parameters (from the form) into a dictionary
		
		parameters = {}
		print "keys are " + str(form.keys())
		
		for key in form.keys():
			parameters[key] = form[key].value
		
		
		# create a response back to the web browser that
		# requested this page.
		# The reply should be a web page.
		
		# Let's peek inside the form object to see what is inside.
		# you should be able to see the cgi variables that are being
		# sent from the form. Thanks Cary!
		
		# print dir(form)
		

		#			self.send_header('Location', 'localhost:34567/hello')
		self.send_response(200)
		self.send_header('Content-type','text/html')	
		self.end_headers()
		
		newURL, method = getController('POST', self.path)
		self.wfile.write(method(parameters))

		return			
			
			
try:
	# Create a web server and define the handler to manage the
	# incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	# Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	