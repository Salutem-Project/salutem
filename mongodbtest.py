# https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
# https://api.mongodb.com/python/current/tutorial.html
# https://kb.objectrocket.com/mongo-db/how-to-access-and-parse-mongodb-documents-in-python-364
# used as guide and reference for this

'''
Store the sub-records in the main document, and also write them to the separate collection
was originally going to do just multiple collections but decided this approach due to 
https://forums.meteor.com/t/on-multiple-collections-vs-embedded-documents/42882/3
'''
from pymongo import MongoClient
from pprint import pprint
import json
class Database_Abstraction():

    def __init__(self):
        # Connect to MongoDB
        client = MongoClient()
        self.database = client.test

        # Collection references
        self.remote =  self.database.remote
        self.station = self.database.station
        self.backend = self.database.backend

    def create_station(self, station_data):
        ''' 
        Places a dictionary of information into the database, expecting specific keys.
        in the format of station_data = {'s_id':1,'location':'Room A'}

        Expected keys:
            's_id': The reference id to the station
            'location':room number or letter
        '''
        if 's_id' in station_data and 'location' in station_data:
    		print "create station gucci"
    		result=self.station.insert_one(station_data)
        	pprint(result)
    	else:
    		print "invalid syntax"
        

    def remove_station(self, station_data):
        ''' 
        Deletes the station from the database using s_id and location
        in the format of station_data = {'s_id':1,'location':'Room A'}
		
		Keys:
			's_id':id for the station
			'location':where the station is 
        '''
        if 's_id' in station_data and 'location' in station_data:
    		print "remote station gucci"
    		result=self.station.delete_one(station_data)
        	pprint(result)
    	else:
    		print "invalid syntax"
    def create_remote(self, remote_data):
    	'''
    	adds new remote data to the remote collection
    	in the format of remote_data = {'r_id':1,'employee':'Jeff'

    	Keys:
    		r_id: id for the remote
    		employee: employees name or employee number

    	'''
    	if 'r_id' in remote_data and 'employee' in remote_data:
    		print "create remote gucci"
    		self.remote.insert_one(remote_data)
    	else:
    		print "invalid syntax"

    def remove_remote(self,remote_name):
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
    		print "invalid syntax"
    def ping(self, remote_name):
    	'''
    	returns the most current remote location based on the last update from update_remote
    	in the format of remote_name = {'r_id':1}
    	'''
    	if 'r_id' in remote_data:
    		print "ping gucci"
    		result=self.remote.find_one(remote_name)
        	pprint(result)
    	else:
    		print "invalid syntax"
    def update_remote(self,remote_data,update_data):
    	'''
    	updates the remote collection with the new remote data
    	will be used to add location data in the UI

    	the update data parameter is just for the new information
    	uses push to keep a history of locations
    	update_data1  = {'$push':{'station':{'s_id':1,'location':'room A', 'signal':1.2}}}

    	'''
    	if 'r_id' in remote_data and '$push' in update_data:
    		print "update gucci"
    		result=self.remote.update_one(remote_data,update_data)
    		pprint(result)
    	else:
    		print "invalid syntax"


if __name__ == '__main__':
    # Creating example data
    remote_data = {'r_id':1,'employee':'Jeff'}
    station_data = {'s_id':1,'location':'Room A'}
    remote_name = {'r_id':1}
    update_data1  = {'$push':{'station':{'s_id':1,'location':'room A', 'signal':1.2}}}
    update_data2  = {'$push':{'station':{'s_id':2,'location':'room B', 'signal':4.0}}}

    foo = Database_Abstraction()
    foo.create_station(station_data)
    foo.remove_station(station_data)
    foo.create_remote(remote_data)
    foo.ping(remote_name)
    foo.update_remote(remote_data,update_data1)
    foo.ping(remote_name)
    foo.update_remote(remote_data,update_data2)
    foo.ping(remote_name)
    foo.remove_remote(remote_name)
    foo.ping(remote_name)