#!/usr/bin/python


#--------------------------------
def routes():
	return (('get', '', ('', 'webController::createWebFormPage')),
			('post', '/', ('/', 'webController::respondToSubmit')),
			
			)


	