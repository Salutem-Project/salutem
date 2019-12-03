# Parsing API request information
from flask_restful import reqparse, Resource

# Standard packages
from os.path import join

# Local modules
from Database import DatabaseAbstractionLayer
from settings import getAPISettings

class _SalutemAPI(Resource):
	def get(self):
		return "Hello, World"

	def _createDatabase(self, salutemSettings):
		# Creating an instance of the database with out database settings in mind
		self._database = DatabaseAbstractionLayer(salutemSettings)

	def _parseArguments(self, argumentList):
		parser = reqparse.RequestParser()
		for argument in argumentList:
			parser.add_argument(argument)
		return parser.parse_args()

	def _setupEndpoint(self, argumentList=None):
		# Creating a database in self._database
		self._createDatabase(getAPISettings(join('assets', 'databaseSettings.json')))
		# Returning arguments parsed from an argument list
		return self._parseArguments(argumentList) if argumentList is not None else None
