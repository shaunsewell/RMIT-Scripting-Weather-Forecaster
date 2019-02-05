#!/usr/bin/python


import sys
import importlib

from routes import routes

#--------------------------------
def getController(method, path):
	for each in routes():
		# each looks like ('get', '/', ('/index.html', 'things::wow'))
		if each[0].lower() == method.lower() and each[1] == path:
			(newPath, moduleController)  = each[2]
			break
	else:
		# didn't find a match
		# should create a 404 page instead of an exception
		raise ValueError("No such path")

	middle =  moduleController.find('::');
	
	# get the module name
	moduleName = moduleController[:middle]
	# get the function name
	controllerName = moduleController[middle + 2:]


	module  = importlib.import_module(moduleName)
	methodToCall = getattr(sys.modules[moduleName], controllerName)


	return (newPath, methodToCall)