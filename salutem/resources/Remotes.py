# Parsing API request information
from flask_restful import reqparse

# Local modules
from SalutemAPI import _SalutemAPI
from settings import getAPISettings

class Remotes(_SalutemAPI):
	''' API access to data pertaining to remote security devices.

		Arguments:
			remoteID | string:
				The unique identifier for the remote.

		Methods:
			post - Register a remote to a userID
			delete - De-register a remote device from any user
			put - Register a single ping from a remote device to a base station
			get - Gets the current location information from a give remote
	'''
	def post(self, remoteID):
		''' Register a remote to a userID.

			Payload:
				userID | string:
					The unique identifier for the user that has "checked out" the remote.
		'''
		args = self._setupEndpoint(['userID'])
		# Registering this information with the database
		self._database.registerDevice(args['userID'])

	def delete(self, remoteID):
		''' De-register a remote device from any user.
		'''
		_ = self._setupEndpoint()
		# Clearing all user information from the remote
		self._database.registerDevice(None)

	def put(self, remoteID):
		''' Register a single piece of information to determine the location of a remote.

			Payload:
				baseStationID | string:
					The ID for the base station sending the ping.
				signalStrength | string:
					The signal strength of the remote device from the base station that is sending the information.
				status | int:
					The status that the current remote is transmitting.
		'''
		args = self._setupEndpoint([
			'baseStationID',
			'signalStrength',
			'priority',
		])
		# Recording record with our database
		self._database.recordPing(remoteID, **args)

	def get(self, remoteID=None):
		''' Gets the location information for the remoteID in question.

		'''
		args = self._setupEndpoint()
		# Collecting location of remote
		return self.locateRemote(remoteID)

	def locateRemote(self, remoteID=None):
		''' Returns the (x, y) coords of the referenced remote.

			self._database has to already be configured.

			Arguments:
				remoteID | string:
					The remote ID in question.
		'''
		#@TODO actually calculate the location of the remote device.
		pass
