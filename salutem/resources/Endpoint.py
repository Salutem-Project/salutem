# Parsing API request information
from flask_restful import reqparse, Resource
from flask import request

# Standard packages
from os.path import join

# Local modules
from salutem.Database import DatabaseAbstractionLayer
from salutem.settings import getAPISettings

class _SalutemAPI(Resource):
    def get(self):
        return "Hello, World"

    def _createDatabase(self):
        # Creating an instance of the database with out database settings in mind
        self._database = DatabaseAbstractionLayer()

    def _parseArguments(self, argumentList):
        parser = reqparse.RequestParser()
        print(request.headers, flush=True)
        for argument in argumentList:
            parser.add_argument(argument)
        return parser.parse_args()

    def _setupEndpoint(self, argumentList=None):
        print('setting up endpoint', flush=True)
        # Creating a database in self._database
        self._createDatabase()
        print('database created')
        # Returning arguments parsed from an argument list
        print(argumentList)
        if argumentList is None:
            print('arugment is none')
            return None
        else:
            print('parsing arguments')
            return self._parseArguments(argumentList)
