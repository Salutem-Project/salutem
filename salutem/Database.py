#!/bin/env python36

# https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
# https://api.mongodb.com/python/current/tutorial.html
# https://kb.objectrocket.com/mongo-db/how-to-access-and-parse-mongodb-documents-in-python-364
# used as guide and reference for this
#https://stackoverflow.com/questions/37941610/get-all-documents-of-a-collection-using-pymongo

'''
Store the sub-records in the main document, and also write them to the separate collection
was originally going to do just multiple collections but decided this approach due to
https://forums.meteor.com/t/on-multiple-collections-vs-embedded-documents/42882/3
'''
from pymongo import MongoClient
from pprint import pprint
from salutem.tri import trilaterate
import json

class DatabaseAbstractionLayer():

    def __init__(self):
        # Connect to MongoDB
        client = MongoClient()
        self.database = client.data

        # Collection references
        self.remote =  self.database.remote
        self.station = self.database.station
        self.backend = self.database.backend

    def _parse_to_JSON(self, package):
        package['_id'] = str(package['_id'])

   # Remote
   #####################################
    def create_remote(self, remote_data):
        '''
        adds new remote data to the remote collection
        in the format of remote_data = {'r_id':1,'employee':'Jeff'
        Keys:
            r_id: The remotes unique identifier
            u_id: The user's id code or unique identifier
        '''
        if ('r_id' in remote_data) and ('u_id' in remote_data):
            self.remote.insert_one(remote_data)
        else:
            print("invalid syntax")
        data = self.ping(remote_data)
        return self._parse_to_JSON(data)

    def remove_remote(self, remote_data):
        '''
        for end of day cleaning of remote for next day
        in the format of remote_data = {'r_id':1}
        Keys:
            r_id: id for the remote
        '''
        if ('r_id' in remote_data):
            result=self.remote.delete_many(remote_data)
            pprint(result)
        else:
            print("invalid syntax")

    def update_remote(self, remote_data, update_data):
        '''
        updates the remote collection with the new remote data
        will be used to add location data in the UI
        the update data parameter is just for the new information
        uses push to keep a history of locations
        update_data1  = {'$push':{'station':{'s_id':1,'location':'room A', 'signal':1.2}}}
        Should expect a dictionary with the following keys:
            'r_id': The remote's unique identifier that the station picked up
            's_id': The stations unique identifier of the reporting station
            'signal': The strength of the signal received from the station

        This should have a single input dictionary with the minimal information required to put into the database.
        If the database function requires more information in the dictionary that is the same every time, that should be done inside this function.
        '''
        if ('r_id' in remote_data):
            result = self.remote.update_one(remote_data, {'$push': update_data})
            pprint(result)
        else:
            print("invalid syntax")
        data = self.ping(remote_name)
        return self._parse_to_JSON(data)

    def ping(self, remote_data):
        '''
        returns the most current remote location based on the last update from update_remote
        in the format of remote_data = {'r_id':1}
        '''
        if ('r_id' in remote_data):
            return self.remote.find_one(remote_data)
        else:
            print("invalid syntax")

    def find_remote(self,remote_data):
        '''
        data is a dict of the remote data
        location is a list of signals in the remote data returned by dict.get
        trilaterare returns the index of the closest station in that original list of signal
        '''
        data = self.ping(remote_data)
        location = data.get(u'station')
        index = trilaterate(location)
        print("remote location is in", end=" ")
        pprint(location[index].get(u'location'))

   # Station
   #####################################
    def create_station(self, station_data):
        '''
        Places a dictionary of information into the database, expecting specific keys.
        in the format of station_data = {'s_id':1,'location':'Room A'}
        Expected keys:
            's_id': The reference id to the station
            'location':room number or letter
        '''
        if all([key in station_data for key in ['s_id', 'location', 'x_cord', 'y_cord']]):
            result = self.station.insert_one(station_data)
            pprint(result)
        else:
            print("invalid syntax")
        data = self.station.find_one(station_data)
        return data

    def remove_station(self, station_data):
        '''
        Deletes the station from the database using s_id and location
        in the format of station_data = {'s_id':1,'location':'Room A'}
        Keys:
           's_id':id for the station
           'location':where the station is
        '''
        if ('s_id' in station_data):
            result = self.station.delete_one(station_data)
            pprint(result)
        else:
            print("invalid syntax")

   # Print functions
   #####################################
    def get_remotes(self):
        '''
        Returns a list of all remote collections as python dictionaries.
        '''
        return [_parse_to_JSON(_) for _ in self.remote.find()]

    def get_stations(self):
        '''
        Returns a list of all station collections as python dictionaries.
        '''
        return [_parse_to_JSON(_) for _ in self.station.find()]

    def get_all(self):
        '''
        print all objects in both remote and station to screen
        '''
        return self.get_remotes() + self.get_stations()

if __name__ == '__main__':
     # Creating instance of database
    foo = DatabaseAbstractionLayer()

    # Declaring example remote data
    remote_test_data_1 = {'r_id': '1', 'u_id': '11'}
    remote_test_data_2 = {'r_id': '2', 'u_id': '12'}
    remote_test_data_3 = {'r_id': 3, 'u_id': 13}

    # Adding some remotes
    foo.create_remote(remote_test_data_1)
    foo.create_remote(remote_test_data_2)

    # @TODO Check if remotes 1 & 2 are in the database

    # Removing remote 2 and adding 3, leaving 1 & 3 in the database
    foo.remove_remote({'r_id': 2})
    foo.create_remote(remote_test_data_3)

    # @TODO Check if remote 1 and 3 are in the database

    # Declaring example station data
    station_test_data_1 = {'s_id': 1, 'location':'Room A', 'x_cord':200.3, 'y_cord': 100.01}
    station_test_data_2 = {'s_id': 2, 'location':'Room B', 'x_cord':370.83, 'y_cord': 73.92}
    station_test_data_3 = {'s_id': 3, 'location':'Room B', 'x_cord':4.73, 'y_cord': 109.34}

    # Adding some stations
    foo.create_station(station_test_data_1)
    foo.create_station(station_test_data_2)

    # @TODO Check if stations 1 & 2 are in the database

    # Removing station 2 and adding 3, leaving 1 & 3 in the database
    foo.remove_station({'s_id': 2})
    foo.create_remote(remote_data_test_3)

    # @TODO Check if station 1 & 3 are in the database
