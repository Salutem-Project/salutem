#!/bin/env python37

# Flask server modules
from flask import Flask
from flask_restful import Api, Resource, reqparse

# Local modules
from resources.Remotes import Remotes

# Creating our application and API
app = Flask(__name__)
api = Api(app)

# API endpoints
api.add_resource(Remotes, "remote/<string:remoteID>")

# Running the Application
app.run(debug=True)