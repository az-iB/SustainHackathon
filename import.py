
import re
import urllib2
from bs4 import BeautifulSoup
import dateutil.parser as dparser
import pymongo
from pymongo import MongoClient
import json
import socket
import logging
import time


connection = MongoClient('mongodb://localhost:27017')

db = connection.chargeHistory

def importData():
    # open data file for import
    i = 0;
    newEntry = dict();
    for line in open('data', 'r'):
        line = re.sub('\s+', ' ', line)
        #print i, ">> ", line

        flag = i % 5
        if flag == 0:
            if i != 0: # first time has no content
                #print newEntry
                db.collections.insert( newEntry );
            newEntry.clear()
            newEntry['stationID'] = line
            
        elif flag == 1:
            newEntry['Address'] = line

        elif flag == 2:
            newEntry['startTime'] = line

        elif flag == 3:
            newEntry['endTime'] = line

        elif flag == 4:
            newEntry['recordNumber'] = line
            
        i += 1

# XXX should be replace by a background job on server
# regularly collects the data for mining.
#importData()
