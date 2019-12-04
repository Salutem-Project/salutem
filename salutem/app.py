#!/bin/env python37

# Flask server modules
from flask import Flask
from flask_restful import Api, Resource, reqparse

# Local modules
import Remotes

class salutemAPI():
	def __init__(self):
		global FLASK_APP, FLASK_API

		# Creating our application and API
		FLASK_APP = Flask(__name__)
		FLASK_API = Api(FLASK_APP)

		# API endpoints
		FLASK_API.add_resource(Remotes.Remotes, "/remote/<string:remoteID>")
		from SalutemAPI import _SalutemAPI as coverpage
		FLASK_API.add_resource(coverpage, "/")

if __name__ == "__main__":
	_ = salutemAPI()
	# Running the application
	global FLASK_API
	FLASK_APP.run(host='0.0.0.0', port=1080, debug=True)