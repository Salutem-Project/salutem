#!/bin/env python36

# https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
# https://api.mongodb.com/python/current/tutorial.html
# https://kb.objectrocket.com/mongo-db/how-to-access-and-parse-mongodb-documents-in-python-364
# used as guide and reference for this
# https://stackoverflow.com/questions/37941610/get-all-documents-of-a-collection-using-pymongo

'''
Store the sub-records in the main document, and also write them to the separate collection
was originally going to do just multiple collections but decided this approach due to
https://forums.meteor.com/t/on-multiple-collections-vs-embedded-documents/42882/3
'''
# Standard modules
import json
from statistics import mean

# Pypi modules
from pymongo import MongoClient

class DatabaseAbstractionLayer():

    def __init__(self):
        ''' A logical abstraction layer for a mongoDB database.
        '''
        # Connect to MongoDB
        client = MongoClient()
        self.database = client.data

        # Collection references
        self._remote =  self.database.remote
        self._station = self.database.station
        self._backend = self.database.backend

        # The number of pings to keep for any given remote
        self.max_pings = 20

   # Helper functions
   #####################################
    def _parse_to_JSON(self, package):
        package['_id'] = str(package['_id'])
        return package

   # Remote
   #####################################
    def create_remote(self, remote_id, user_id, additional_data={}):
        ''' Inserts a record into the remote collection.

            Arguments:
                remote_id (str): The remote's unique identifier
                user_id (str): The user's id code or unique identifier
                additional_data (dict): Additional data in the form of a dictionary to add to the record (default = {})

            Returns:
                The record of the remote that was added
        '''
        # Removing _id if needed
        if '_id' in additional_data:
            del additional_data['_id']
        # Placing our required arguments into our dictionary
        additional_data['r_id'] = str(remote_id)
        additional_data['u_id'] = str(user_id)
        # Placing our dictionary into the database
        self._remote.insert_one(additional_data)
        # Returning the record of the added remote
        from pprint import pprint
        # pprint('Remote = ' + {self.get_remotes(remote_id)})
        return self._parse_to_JSON(self.get_remotes(remote_id))

    def remove_remote(self, remote_id):
        ''' Removes remotes that have the given remote ID.
            NOTICE: This does not prompt for deletion. Make sure you want to delete these records before you do so.

            Arguments:
                remote_id (str): The ID of the remote to delete documents from the database

            Returns:
                How many documents were deleted.
        '''
        result = self._remote.delete_many({'r_id': str(remote_id)})
        # Returning the number of documents deleted
        return result.deleted_count

    def ping_remote(self, r_id, s_id, signal, status):
        ''' Adds signal information to the specified remote.

            Arguments:
                r_id (str): The remote's ID that the signal collected
                s_id (str): The station's ID that is sending the signal
                signal (str): The signal strength from the remote
        '''
        # First, we check to see if our ping limit has been reached
        doc = self.get_remotes(r_id)
        if 'pings' not in doc.keys():
            doc['pings'] = []
        if len(doc['pings']) < self.max_pings:
            result = self._remote.update_many(
                {'r_id': r_id},   # Filtering to only find remotes with this ID
                {'$push': {'pings':    # Pushing data onto a key called 'pings'
                    {'s_id': s_id, 'signal': signal}
                }}
            )

        # Our ping limit has been reached, we gotta fix that
        else:
            # Inserting our new ping into the first position of the pings list
            doc['pings'].insert(0, {
                's_id': s_id,
                'signal': signal
            })
            # Setting our new list (only the first self.max_pings entries) into the database
            result = self._remote.update_many(
                {'r_id': r_id},   # Filtering to only find remotes with this ID
                {'$set': {'pings':
                    doc['pings'][:self.max_pings]
                }}
            )

        # Returning the updated documents
        self._trilaterate_remote(r_id)
        return self.get_remotes(r_id)

    def _trilaterate_remote(self, remote_id):
        ''' Finds the suggested location of the remote using some fancy trilateration.

        Arguments:
            remote_id (str): The remote ID for which to find the location
        '''
        # First thing, we're going to find our ping location
        doc = self.get_remotes(remote_id)

        # Creating a record of stations to add our pings
        station_data = {}

        # Doing this with each ping
        for data in doc['pings']:
            if data['s_id'] not in station_data.keys():
                station_data[data['s_id']] = {'pings': []}
            station_data[data['s_id']]['pings'].append(int(data['signal']))

        # Averaging each signal
        for station, data in station_data.items():
            station_data[station]['signal'] = mean(data['pings'])
            # Finding the stations location for each station
            station_doc = self.get_stations(station)
            data['x_cord'] = station_doc['x_cord']
            data['y_cord'] = station_doc['y_cord']

        # Finding our average signal to move our center point
        average_signal = mean([data['signal'] for _, data in station_data.items()])
        average_location = [
            mean([int(data['x_cord']) for _, data in station_data.items()]),
            mean([int(data['y_cord']) for _, data in station_data.items()]),
        ]

        # Moving our average location depending on the signal
        location = average_location
        for station_id, data in station_data.items():
            # Finding our difference and scale
            x = (int(data['x_cord']) - average_location[0]) * (int(data['signal']) / average_signal)
            y = (int(data['y_cord']) - average_location[1]) * (int(data['signal']) / average_signal)
            # Adding these values to our suggested location
            location[0] += x
            location[1] += y

        # Updating the location of our remote with our new suggested location
        self._remote.update_many(
            {'r_id': remote_id},
            {'$set': {'location': location}}
        )

   # Station
   #####################################
    def create_station(self, station_id, x_cord, y_cord, additional_data={}):
        ''' Creates a document with the stations data.

            Arguments:
                station_id (str): The ID of the station to be added to the database
                x_cord (float): The location on the x-axis of the given station
                y_cord (float): The location on the y-axis of the given station
                additional_data (dict): Additional data in the form of a dictionary to add to the record (default = {})
        '''
        # Removing _id if needed
        if '_id' in additional_data:
            del additional_data['_id']
        # Placing our required arguments into our dictionary
        additional_data['s_id'] =   str(station_id)
        additional_data['x_cord'] = str(x_cord)
        additional_data['y_cord'] = str(y_cord)

        # Placing our dictionary into the database
        self._station.insert_one(additional_data)
        # Returning the record of the added station
        return self._parse_to_JSON(self.get_stations(station_id))

    def remove_station(self, station_id):
        ''' Removes station that have the given station ID.
            NOTICE: This does not prompt for deletion. Make sure you want to delete these records before you do so.

            Arguments:
                station_id (str): The ID of the station to delete documents from the database

            Returns:
                How many documents were deleted.
        '''
        result = self._station.delete_many({'s_id': str(station_id)})
        # Returning the number of documents deleted
        return result.deleted_count

   # Print functions
   #####################################
    def get_remotes(self, remote_id=None):
        ''' Returns a list of all remote documents as python dictionaries.

        Arguments:
            remote_id (str): The ID of remote's record to get

        Returns:
            An array of all remote documents if no remote ID was specified, otherwise a single remote document.
        '''
        print(f'Getting a remote {remote_id}')
        if remote_id is None:
            return [self._parse_to_JSON(_) for _ in self._remote.find()]
        else:
            return self._parse_to_JSON(self._remote.find_one({'r_id': str(remote_id)}))

    def get_stations(self, station_id=None):
        ''' Returns a list of all station documents as python dictionaries.

        Arguments:
            remote_id (str): The ID of stations's record to get

        Returns:
            An array of all station documents if no station ID was specified, otherwise a single station document.
        '''
        if station_id is None:
            return [self._parse_to_JSON(_) for _ in self._station.find()]
        else:
            return self._parse_to_JSON(self._station.find_one({'s_id': str(station_id)}))

    def get_all(self):
        ''' Returns all remote and station documents from the database.
        '''
        return self.get_remotes() + self.get_stations()

if __name__ == '__main__':
     # Creating instance of database
    foo = DatabaseAbstractionLayer()

    # Flushing the database
    for remote in foo.get_remotes():
        foo.remove_remote(remote['r_id'])
    for station in foo.get_stations():
        foo.remove_station(station['s_id'])

    # Printing a hopefully empty database
    from pprint import pprint
    pprint(foo.get_all())

    # Declaring example remote data
    remote_test_data_1 = {'r_id': '1', 'u_id': '11'}
    remote_test_data_2 = {'r_id': 2, 'u_id': '12'}
    remote_test_data_3 = {'r_id': 3, 'u_id': 13}

    # Adding some remotes
    foo.create_remote(*remote_test_data_1.values())
    foo.create_remote(*remote_test_data_2.values())

    bar = foo.get_remotes()
    for remote in bar:
        del remote['_id']
    baz = [remote_test_data_1, remote_test_data_2]
    assert(bar == baz)

    # Removing remote 2 and adding 3, leaving 1 & 3 in the database
    foo.remove_remote(2)
    foo.create_remote(*remote_test_data_3.values())

    bar = foo.get_remotes()
    for remote in bar:
        del remote['_id']
    baz = [remote_test_data_1, remote_test_data_3]
    assert(bar == baz)

    # Declaring example station data
    station_test_data_1 = {'s_id': 1, 'x_cord':200.3, 'y_cord': 100.01}
    station_test_data_2 = {'s_id': 2, 'x_cord':370.83, 'y_cord': 73.92}
    station_test_data_3 = {'s_id': 3, 'x_cord':4.73, 'y_cord': 109.34}

    # Adding some stations
    foo.create_station(*station_test_data_1.values())
    foo.create_station(*station_test_data_2.values())

    bar = foo.get_stations()
    for station in bar:
        del station['_id']
    baz = [station_test_data_1, station_test_data_2]
    assert(bar == baz)

    # Removing station 2 and adding 3, leaving 1 & 3 in the database
    foo.remove_station(2)
    foo.create_station(*station_test_data_3.values())

    bar = foo.get_stations()
    for station in bar:
        del station['_id']
    baz = [station_test_data_1, station_test_data_3]
    assert(bar == baz)

    print('Passed Unit Test!!!!!!!!!! :)')
