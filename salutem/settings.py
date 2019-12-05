# Standard modules
from json import load

# Simple function to read setting in from json file
def getAPISettings(file):
	with open(file) as configFile:
		return configFile.load()