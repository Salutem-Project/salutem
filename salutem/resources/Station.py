# Local modules
from salutem.resources.Endpoint import _SalutemAPI
from salutem.settings import getAPISettings

from datetime import datetime

# This module does its best to use a modified google docstring standard - https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

class Station(_SalutemAPI):
	def post(self, stationID):
		try:
			args = self._setupEndpoint(['location'])
			args['s_id'] = stationID
			# Registering this information with the database
			stationInfo = self._database.create_station(args)
			# Returning success
			return stationInfo, 200
		except:
			# Unable to register the device for some reason - internal server error
			return('Device could not be registered.', 500)

	def delete(self, stationID):
		''' De-register a stations device from any user.

			Payload: - None

			Returns:
				Name of the station ID deleted and 200 on success, otherwise a 500
		'''
		try:
			_ = self._setupEndpoint()
			# Clearing all user information from the remote
			self._database.remove_remote({'s_id': stationID})
			# Returning success
			return f'{stationID} successfully de-registered', 200
		except ValueError:
			# Station not found, no need to delete record - success
			return('Device not found.', 200)
		except:
			# Station unable to de-register for some reason - internal server error
			return('Unable to delete device.', 500)

