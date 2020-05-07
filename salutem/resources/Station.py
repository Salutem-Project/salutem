# Local modules
from salutem.resources.Endpoint import _SalutemAPI
from salutem.settings import getAPISettings

from datetime import datetime

# This module does its best to use a modified google docstring standard - https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

class Station(_SalutemAPI):
    def post(self, stationID):
        ''' Add a station to the database.

            Payload:
                x_cord: The location on the x-axis of the station
                y_cord: The location on the y-axis of the station

            Returns:
                Information about the remote given from the database. 200 on successful registration.
                Otherwise, returns a 500 code.
                HTTP status codes - https://www.restapitutorial.com/httpstatuscodes.html
        '''
        try:
            # Collecting arguments from the payload
            args = self._setupEndpoint(['x_cord', 'y_cord'])
            # Registering this information with the database
            remoteInfo = self._database.create_station(stationID, *args)
            # Returning success
            return remoteInfo, 200
        except:
            # Unable to register the device for some reason - internal server error
            return('Device could not be registered.', 500)

    def delete(self, stationID):
        ''' Delete a station from the database

            Payload: - None

            Returns:
                Name of the station ID deleted and 200 on success, otherwise a 500
        '''
        try:
            # Setting up our endpoint
            self._setupEndpoint()
            # Clearing all user information from the remote
            count = self._database.remove_station(stationID)
            # Returning success
            return f'Successfully deleted {count} stations with the id {stationID}.', 200
        except ValueError:
            # Station not found, no need to delete record - success
            return('Device not found.', 200)
        except:
            # Station unable to de-register for some reason - internal server error
            return('Unable to delete device.', 500)

