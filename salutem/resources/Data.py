# Local modules
from salutem.resources.Endpoint import _SalutemAPI
from salutem.settings import getAPISettings

from datetime import datetime

# This module does its best to use a modified google docstring standard - https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

class Data(_SalutemAPI):
    ''' API access to data pertaining to remote security devices.

        Arguments: The API will have the same argument for each operator, so I'll only specify it this once. Instead, the documentation for each operator will include a 'payload' section that wil act vary similar.
            remoteID (str): The ID for the remote that the base station is reporting.

        Attributes:
            _database (:obj:`Database`): Database abstraction layer to store data.
    '''
    def get(self, group):
        ''' Get data from a group

            Payload: None

            Returns:
                A list of python dictionaries inside a dictionary with they key as the group
                    i.e. post('stations') --> `{'stations': [<list of station information>]}`
                Otherwise, returns a 500 code.
                HTTP status codes - https://www.restapitutorial.com/httpstatuscodes.html
        '''
        print(f'Retriving data for group {group}')
        print(group.lower())
        try:
            print('Attempting to setup endpoint')
            self._setupEndpoint()
            print('Endpoint setup')
            if (group.lower() in ['remote', 'remotes']):
                print('Matched remotes')
                foo = {
                    group: self._database.get_remotes()
                }
                from pprint import pprint
                pprint(foo)
                return (foo, 200)
              #return ({group: self._database.get_remotes()}, 200)
            if (group.lower() in ['station', 'stations']):
                print('Matched sations')
                return ({group: self._database.get_stations()}, 200)
            if (group.lower() in ['*', 'all', '_', '']):
                print('Matched all')
                return ({group: self._database.get_all()}, 200)
        except:
            # Unable to register the device for some reason - internal server error
            return(f'No group named {group}', 500)
