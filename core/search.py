
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
import math

class Choice():
    def __init__(self, addr, dist):
        self.address = addr
        self.distance = dist

############## Helper functions #########

def yieldRawMinute(startHMS, offset = 0):
    # HM = Hour:Minute
    #print startHMS, '==', endHMS
    startHM = startHMS[:5]
    startH = int(startHM.split(':')[0])
    startM = int(startHM.split(':')[1])
    #print startH, startM
    start  = startH*60 + startM + offset
    #print start

    return start

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

# used to sort first based on hitRate and then based on distance
# as we treat all distance within 300m the same
def multikeysort(items, columns):
    from operator import itemgetter
    comparers = [ ((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1)) for col in columns]  
    def comparer(left, right):
        for fn, mult in comparers:
            result = cmp(fn(left), fn(right))
            if result:
                return mult * result
            else:
                return 0
    return sorted(items, cmp=comparer)


############## core function ###############

# return: distance, address (rating?)
def searchDistanceWithMining(request, dateTime):

    # connecting to mongo db
    connection = MongoClient('mongodb://10.34.18.181:27017')
    db = connection.chargeHistory

    collections = db.collections.find()

    stations = dict();
    # initialize station list
    #for entry in collections:
        #stations[entry['stationID']] = 0

    # XXX changeMe
    targetTime = dateTime
    targetStart = yieldRawMinute(targetTime, -10)
    targetEnd   = yieldRawMinute(targetTime, +10)


    for entry in collections:
        stationID_ = entry['stationID'].strip()
        if stationID_ not in stations:
            stations[stationID_] = 0
        #print entry
        # HMS = Hour:Minute:Second
        startHMS = entry['startTime'].split(' ')[1]
        endHMS   = entry['endTime'].split(' ')[1]

        start = yieldRawMinute(startHMS)
        end = yieldRawMinute(endHMS)

        #print startHMS, '->', endHMS, '  ', start, '->', end,
        
        # core comparison logic
        # case 1: start < targetStart < end
        # case 2: start < targetEnd < end
        if start < targetStart and targetStart < end:
            #print '@@', stationID_
            stations[stationID_] += 1
        elif start < targetEnd and targetEnd < end:
            #print '@@', stationID_
            stations[stationID_] += 1
        else:
            d = None
            #print

        # offset
        start = 0
        end = 0

    print
    print 'Total sessions to be mined:', collections.count()
    print 'Targeted start/end umbrella', targetStart, targetEnd
    print

    # this stations dictionary contains a stationID -> queryHitCount mapping
    print
    print 'stationID -> HitCount based on query'
    print
    #for ha in stations:
        #print ha

    from getPublicStation import getPublicStations

    # return a list of nearby charging stations

    request = "442 N Canon Dr Beverly Hills"

    from pygeocoder import Geocoder
    results = Geocoder.geocode(request) 
    destLat, destLng = results[0].coordinates

    results = getPublicStations(destLat, destLng)
    stationsHit = results.stationData
    #print stationsHit

    import sys

    # sort based on distance
    # practically, they're already actually in distance order
    # since getPublicStations will return so.
    # but we still need to calculate the distance for UI display

    print
    print 'Calculating distance and combining the view with hitRate..'
    print
    for station in stationsHit:

        # measured in kilometers
        diff = distance([ destLat, destLng],
                        [ float(station.Port[0].Geo.Lat),
                          float(station.Port[0].Geo.Long) ])
        diff = diff / 1.6
        setattr(station, 'distance', diff)

        rating = 0
        if station.stationID in stations:
            setattr(station, 'hitRate', stations[station.stationID])

            # XXX simple yet working formula
            rating = station.distance + station.hitRate/30.0
            setattr(station, 'rating', rating)

        else:
            # we found the station in getPublicStations but somehow
            # we couldn't locate it from our session history for duration = 1 month
            # there's probably something wrong, so we don't show them
            setattr(station, 'hitRate', sys.maxint)
            setattr(station, 'rating', sys.maxint)


        #print station.stationID, ':', station.distance, '->', station.hitRate,   '=', station.rating

    #list_address = []
    #list_distance = []

    list_choices = []

    i = 0;
    finalist = sorted(stationsHit, key=lambda x: x.rating)
    for station in finalist:
        if station.rating != sys.maxint:
            print station.stationID, ':', station.distance, '->', station.hitRate,   '=', station.rating,
            #print float(station.Port[0].Geo.Lat), float(station.Port[0].Geo.Long)
            # we only return the first ten results
            # this should be enough
            if i < 6:
                distanceRound = round(station.distance, 2)
                list_choices.append(Choice(station.Address, distanceRound))
                print
            else:
                print '- dropped'
            i += 1
        
    return list_choices




########################### END ##############

#print
#print 'Now the segregated multiKey sorting to find our finalist..'
#print

# sort first based on hitRate (the less the better)
# and then sort based on distance (within certain distance range: 300m)

def segregatedMultiKeySort(stationsHit, columns, segregateRange = 0.3):

    aList = [];

    for i in range(int(1/segregateRange)):

        for station in stationsHit:
            if station.distance > (i*segregateRange) and station.distance < (i+1)*segregateRange:
                # in between the range
                aList.append(station)

        a = multikeysort(aList, ['hitRate', 'distance'])

    return a

#for station in a:
    #print station.stationID, ':', station.distance, '->', station.hitRate

