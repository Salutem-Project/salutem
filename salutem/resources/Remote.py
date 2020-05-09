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
        ''' Add a remote to the database.

            Payload:
                u_id: The user's id code or unique identifier

            Returns:
                Information about the remote given from the database. 200 on successful registration.
                Otherwise, returns a 500 code.
                HTTP status codes - https://www.restapitutorial.com/httpstatuscodes.html
        '''
        try:
            # Collecting arguments from the payload
            args = self._setupEndpoint(['u_id', 'additional_data'])
            # Making additional data a dictionary
            args['additional_data'] = ast.literal_eval(args['additional_data'].replace('\'', '\"')) if args['additional_data'] != '{}' else {}
            # Registering this information with the database
            remoteInfo = self._database.create_remote(remoteID, *args.values())
            # Returning success
            return remoteInfo, 200
        except:
            # Unable to register the device for some reason - internal server error
            return('Device could not be registered.', 500)

    def delete(self, remoteID):
        ''' Delete a remote from the database.

            Payload: - None

            Returns:
                Name of the remote ID deleted and 200 on success, otherwise a 500
        '''
        try:
            # Setting up our endpoint
            self._setupEndpoint()
            # Clearing all user information from the remote
            count = self._database.remove_remote(remoteID)
            # Returning success
            return f'Successfully deleted {count} remotes with the id {remoteID}.', 200
        except ValueError:
            # Remote not found, no need to delete record - success
            return('Device not found.', 200)
        except:
            # Remote unable to de-register for some reason - internal server error
            return('Unable to delete device.', 500)

    def put(self, remoteID):
        ''' Register a single piece of information to determine the location of a remote.

            Payload:
                s_id (str): The ID for the base station sending the ping.
                signal (str): The signal strength of the remote device from the base station that is sending the information.
        '''
        try:
            # Setting up our endpoint by getting some arguments
            args = self._setupEndpoint(['s_id', 'signal'])
            # Recording record with our database
            self._database.ping_remote(remoteID, *args.values())
            # Returning success
            return('Data successfully delivered.', 200)
        except:
            # Unable to store information about remote - internal server error
            return('Unable to record information.', 500)

    def get(self, remoteID):
        ''' Gets the current information pertaining from the given remote ID from the database.

            When remoteID is '*', this return the location of every remote.

            Returns:
                A list of python dictionaries inside a dictionary with they key as the group
                    i.e. post('stations') --> `{'stations': [<list of station information>]}`
                Otherwise, returns a 500 code.
                HTTP status codes - https://www.restapitutorial.com/httpstatuscodes.html        '''
        try:
            # Setting up our endpoint
            self._setupEndpoint()    # This doesn't need a value to be set as it won't return any arguments

            # If this is a wildcard, we'll return all the remotes
            if remoteID == '*':
                return (self._database.get_remotes(), 200)
            # Otherwise, we're going to return the remote that the use asked for
            else:
                return (self._database.get_remotes(remoteID), 200)

        except:
            # Unable to gather information about locations - internal server error
            return('Remotes can not be found', 500)