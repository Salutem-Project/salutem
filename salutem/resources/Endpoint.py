# Parsing API request information
from flask_restful import reqparse, Resource
from flask import request

# Standard packages
from os.path import join
from datetime import datetime

# Local modules
from salutem.Database import DatabaseAbstractionLayer
from salutem.settings import getAPISettings

class _SalutemAPI(Resource):
    def _log(self, message):
        print(datetime.now().strftime('[%d/%m/%y %H:%M:%S] ') + f' {self.__class__.__name__}: {message}')

    def _parseArguments(self, argumentList):
        parser = reqparse.RequestParser()
        for argument in argumentList:
            parser.add_argument(argument)
        return parser.parse_args()

    def _setupEndpoint(self, argumentList=None):
        # Creating a reference to the database
        self._database = DatabaseAbstractionLayer()
        # Returning arguments parsed from an argument list
        if argumentList is not None:
            return self._parseArguments(argumentList)
        else:
            return None
        # return self._parseArguments(argumentList) if (argumentList is not None) else None