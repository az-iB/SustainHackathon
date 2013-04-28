
"""
	This examples uses a lightweight soap-based client called Suds for Python.
	
	To install: sudo easy_install suds
	
	Documentation can be found at
	(Cached version)
	http://webcache.googleusercontent.com/search?q=cache:bWwYsuhZSN4J:https://fedorahosted.org/suds/wiki/Documentation+&cd=1&hl=en&ct=clnk&gl=us&client=ubuntu
	
	The following example uses the 'getPublicStations' service to fetch stations within a proximity of 5 Miles.
	"""

__author__ = "Anubhav Agarwal"
__email__ = "anubhav.agarwal@chargepoint.com"


import suds
from suds.client import Client
from suds.wsse import *




# to enable logging, un-comment the following lines
#import logging
#logging.basicConfig(level=logging.DEBUG)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
#logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

def main():
    request = "442 N Canon Dr Beverly Hills"

    from pygeocoder import Geocoder
    results = Geocoder.geocode(request) 
    destLat, destLng = results[0].coordinates

    url = 'https://webservices.chargepoint.com/webservices/chargepoint/services/4.1'
    wsdl = 'https://webservices.chargepoint.com/webservices/chargepoint/services/4.1?WSDL'
    # API user and password
    api_user = 'cf0ab4d655f6bc862d96d3860a3a6c4050647df6f28e41348763126'
    api_pass = '5b81161954c6c73577e75716ce8bb6b1'
	
    # create client and add security tokens in the soap header
    client = Client(url=wsdl, location=url)
    security = Security()
    token = UsernameToken(api_user, api_pass)
    security.tokens.append(token)
    client.set_options(wsse=security)
	
    try:
        # un-comment the print statement below to see the list of all published
        # ChargePoint service SOAP methods.
        print client
		
        # getPublicStations() service method accepts a type of 'stationSearchRequest'
        # so first create a stationSearchRequest type object
        # un-comment above print statement to see all the types
        searchQuery = client.factory.create('sessionSearchdata')
        # un-comment next line to see what parameters are supported
        
        # add properties/filter options
        #searchQuery.Address = "80 S 2nd st"
        #searchQuery.City = "San Jose"
        #searchQuery.State = "CA"
        searchQuery.Proximity = 0.6
        searchQuery.proximityUnit = 'M'
        searchQuery.fromTimeStamp = '2013-03-27 00:00:00'
        searchQuery.toTimeStamp = '2013-04-27 00:00:00'
        searchQuery.startRecord = 1

        # create goeData, provide starting point co-ordinates
        geoData = client.factory.create('geoData')
        # XXX we know what address to search for:
        # 345 N Beverly Dr
        # Beverly Dr
        geoData.Lat  = destLat
        geoData.Long = destLng
        searchQuery.Geo = geoData
		
        print searchQuery

        # here is the actual call to the service
        response = client.service.getChargingSessionData(searchQuery)
        #print response.ChargingSessionsData
    
        for data in response.ChargingSessionsData:
            print data.stationID
            print data.Address
            print data.startTime
            print data.endTime
            print data.recordNumber

        while len(response.ChargingSessionsData) %100 == 0:
            #print "more to work on"
            new_start = searchQuery.startRecord + 100
            searchQuery.startRecord = new_start

            response = client.service.getChargingSessionData(searchQuery)
        
            for data in response.ChargingSessionsData:
                print data.stationID
                print data.Address
                print data.startTime
                print data.endTime
                print data.recordNumber

	# do whatever with the data
	# print response
    except suds.WebFault as detail:
        print detail

if __name__=="__main__":
    main()
