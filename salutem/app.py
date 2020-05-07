#!/bin/env python37

# Flask server modules
from flask import Flask
from flask_restful import Api

# Local modules
from salutem.resources.Remote import Remote as RemoteEndpoint
from salutem.resources.Station import Station as StationEndpoint
from salutem.resources.Data import Data as DataEndpoint

# Creating our application and API
FLASK_APP = Flask(__name__)
FLASK_API = Api(FLASK_APP)

# API endpoints
FLASK_API.add_resource(DataEndpoint,  "/<string:group>")
FLASK_API.add_resource(RemoteEndpoint, "/remote/<string:remoteID>")
FLASK_API.add_resource(RemoteEndpoint, "/remotes/<string:remoteID>")
FLASK_API.add_resource(StationEndpoint, "/station/<string:stationID>")
FLASK_API.add_resource(StationEndpoint, "/stations/<string:stationID>")

# Starting the application up if this is the main file
if __name__ == "__main__":
	startAPIApplication()

# Allowing other modules to start an application without knowing how to
def startAPIApplication():
	# Telling the flask application to run and listen on public port 1080
	FLASK_APP.run(host='0.0.0.0', port=int("1080"), debug=True)
	# We specify the int because flasky is picky. It just works so don't touch it
