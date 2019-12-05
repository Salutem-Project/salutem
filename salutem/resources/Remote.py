# Local modules
from salutem.resources.Endpoint import _SalutemAPI
from salutem.settings import getAPISettings

from datetime import datetime

# This module does its best to use a modified google docstring standard - https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

class Remote(_SalutemAPI):
	''' API access to data pertaining to remote security devices.

		Arguments: The API will have the same argument for each operator, so I'll only specify it this once. Instead, the documentation for each operator will include a 'payload' section that wil act vary similar.
			remoteID (str): The ID for the remote that the base station is reporting.

		Attributes:
			_database (:obj:`Database`): Database abstraction layer to store data.
	'''
	def post(self, remoteID):
		''' Register a remote to a userID.

			Payload:
				userID (str): The unique identifier for the user that has "checked out" the remote.

			Returns:
				Information about the remote given from the database. 200 on successful registration.
				Otherwise, returns a 500 code.
				HTTP status codes - https://www.restapitutorial.com/httpstatuscodes.html
		'''
		try:
			args = self._setupEndpoint(['userID'])
			# Registering this information with the database
			remoteInfo = self._database.registerDevice(args['userID'])
			# Returning success
			return remoteInfo, 200
		except:
			# Unable to register the device for some reason - internal server error
			return 'Device could not be registered.', 500

	def delete(self, remoteID):
		''' De-register a remote device from any user.

			Payload: - None

			Returns:
				Name of the remote ID deleted and 200 on success, otherwise a 500
		'''
		try:
			_ = self._setupEndpoint()
			# Clearing all user information from the remote
			self._database.registerDevice(None)
			# Returning success
			return f'{remoteID} successfully de-registered', 200
		except ValueError:
			# Remote not found, no need to delete record - success
			return 'Device not found.', 200
		except:
			# Remote unable to de-register for some reason - internal server error
			return 'Unable to register device.', 500

	def put(self, remoteID):
		''' Register a single piece of information to determine the location of a remote.

			Payload:
				baseStationID (str): The ID for the base station sending the ping.
				signalStrength (str): The signal strength of the remote device from the base station that is sending the information.
				status (int): The status that the current remote is transmitting.
				additional (`:obj:`dict, optional): Any additional information to store in the database
					This information can be additional attachments to the remote and can span from things like heart rate, to the temperature surrounding the remote.
		'''
		try:
			print(f'Putting remote {remoteID}', flush=True)
			args = self._setupEndpoint([
				'baseStationID',
				'signalStrength',
				'priority',
			])
			# Recording record with our database
			# self._database.recordPing(remoteID, **args)

			with open('log.log', 'a') as outfile:
				outfile.write('\n' + str(datetime.now()) + f' | RemoteID: "{remoteID}"\n')

				for key, value in args.items():
					outString = f'   {key}: {value}\n'
					outfile.write(outString)
					# print(outString, flush=True)

			# Returning success
			return 'Data successfully delivered.', 200
		except:
			# Unable to store information about remote - internal server error
			return 'Unable to record information.', 500

	def get(self, remoteID):
		''' Gets the location information for the remoteID in question.

			Note:
				self._database has to already be configured.

			Arguments:
				remoteID (str): When '*', this return the location of every remote.

			Returns:
				dict::
					remoteID:
					|	user: {userinformation}
					|	location: {calculatedRemoteLocation}
					|	additional: {additionalInformation}

				Dictionary contains many keys if all devices are requested.
		'''
		try:
			args = self._setupEndpoint()
			# Creating a locations dictionary to store our remote locations in
			locations = {}

			# Checking for wildcard
			if remoteID == '*':
				# Getting the remote ID's of all the remotes on the system
				remoteIDs = self._database.getRemotes().keys()
			else:
				remoteIDs = remoteID

			# Collecting the location information for each remote
			for remoteID in remoteIDs:
				locations[remoteID] = self.locateRemote(remoteID)

			# Returning success
			return locations, 200

		except:
			# Unable to gather information about locations - internal server error
			return 'Locations can not be found', 500

	def locateRemote(self, remoteID):
		''' Returns the (x, y) coords of the referenced remote.

			Note:
				self._database has to already be configured.

			@TODO:
				Actually calculate the location of the remote data.

			Returns:
				dict::
					remoteID:
					|	user: {userinformation}
					|	location: {calculatedRemoteLocation}
					|	additional: {additionalInformation}
		'''
		pass
