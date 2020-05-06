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
from tri import trilaterate
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
        if 'r_id' in remote_data and 'u_id' in remote_data:
            self.remote.insert_one(remote_data)
        else:
            print("invalid syntax")
        data = self.ping(remote_data)
        return data

    def remove_remote(self, remote_name):
        '''
        for end of day cleaning of remote for next day
        in the format of remote_name = {'r_id':1}
        Keys:
            r_id: id for the remote
        '''
        if 'r_id' in remote_name:
            result=self.remote.delete_many(remote_name)
            pprint(result)
        else:
            print("invalid syntax")

    def update_remote(self,remote_data,update_data):
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
        if 'r_id' in remote_data:
            result=self.remote.update_one(remote_data,{'$push':update_data})
            pprint(result)
        else:
            print("invalid syntax")
        data = self.ping(remote_name)
        return data

    def ping(self, remote_name):
        '''
        returns the most current remote location based on the last update from update_remote
        in the format of remote_name = {'r_id':1}
        '''
        if 'r_id' in remote_data:
            result=self.remote.find_one(remote_name)
            #pprint(result)
            return result
        else:
            print("invalid syntax")

    def find_remote(self,remote_name):
        '''
        data is a dict of the remote data
        location is a list of signals in the remote data returned by dict.get
        trilaterare returns the index of the closest station in that original list of signal        
        '''
        data = self.ping(remote_name)
        location = data.get(u'station')
        index = trilaterate(location)
        print("remote location is in",end = " ")
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
        if 's_id' in station_data and 'location' in station_data:
            result=self.station.insert_one(station_data)
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
        if 's_id' in station_data:
            result=self.station.delete_one(station_data)
            pprint(result)
        else:
            print("invalid syntax")

   # Print functions
   #####################################
    def print_remotes(self):
    '''
    prints all current remotes in the databse to the screen
    '''
    result=self.remote.find()
    for cursor in result:
        pprint(cursor)

    def print_stations(self):
        '''
        prints all current stations in database to screen
        '''
        result=self.station.find()
        for cursor in result:
            pprint(cursor)

    def print_all(self):
        '''
        print all objects in both remote and station to screen
        '''
        result=self.remote.find()
        for cursor in result:
            pprint(cursor)
        result=self.station.find()
        for cursor in result:
            pprint(cursor)

if __name__ == '__main__':
    # Creating example data
    remote_data = {'r_id':1,'u_id':'Jeff/15'}
    station_data = {'s_id':1,'location':'Room A'}
    station_data_example = {'s_id':1,'location':'Room A' , 'x_cord':200 , 'y_cord': 100.01}
    remote_name = {'r_id':1}
    update_data1  = {'station':{'s_id':1,'location':'room A', 'signal':-45}}
    update_data2  = {'station':{'s_id':2,'location':'room B', 'signal':-20}}
    update_data3  = {'station':{'s_id':3,'location':'room C', 'signal':-80}}


    foo = DatabaseAbstractionLayer()
    #creates testing data
    data=foo.create_station(station_data)
    #foo.remove_station(station_data)
    data=foo.create_remote(remote_data)
    foo.ping(remote_name)

    foo.update_remote(remote_data,update_data1)
    foo.update_remote(remote_data,update_data2)
    foo.update_remote(remote_data,update_data3)
    foo.ping(remote_name)
    #:foo.remove_remote(remote_name)
    data = foo.ping(remote_name)
    foo.print_all()
    foo.remove_remote(remote_name)
    foo.remove_station(station_data)
    #foo.find_remote(remote_name)
