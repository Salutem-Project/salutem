# Parsing API request information
from flask_restful import reqparse, Resource
from flask import request

# Standard packages
from os.path import join

# Local modules
from salutem.Database import DatabaseAbstractionLayer
from salutem.settings import getAPISettings

class _SalutemAPI(Resource):
    def _createDatabase(self):
        # Creating an instance of the database with out database settings in mind
        self._database = DatabaseAbstractionLayer()

    def _parseArguments(self, argumentList):
        parser = reqparse.RequestParser()
        for argument in argumentList:
            parser.add_argument(argument)
        return parser.parse_args()

    def _setupEndpoint(self, argumentList=None):
        # Creating a reference to the database
        self._database = DatabaseAbstractionLayer()
        # Returning arguments parsed from an argument list
        if argumentList is None:
            return None
        else:
            return self._parseArguments(argumentList)
