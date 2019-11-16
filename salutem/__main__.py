#!/bin/env python37

# Flask server modules
from flask import Flask
from flask_restful import Api, Resource, reqparse

# Local modules
import Remotes

# Creating our application and API
app = Flask(__name__)
api = Api(app)

# API endpoints
api.add_resource(Remotes.Remotes, "/remote/<string:remoteID>")

# Running the Application
app.run(debug=True)