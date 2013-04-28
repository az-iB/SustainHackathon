
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

#def main():
def getPublicStations( Glat, Glng, nearby = 0.6 ):

    # contact GoogleMap to convert text address into LAT/LONG:
    #from googlemaps import GoogleMaps
    #gmaps = GoogleMaps('AIzaSyAYtKvQoyBIqJ0kCpAI4o1hu4SX3FFsysI')

    #return
	
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
        # print client
		
        # getPublicStations() service method accepts a type of 'stationSearchRequest'
        # so first create a stationSearchRequest type object
        # un-comment above print statement to see all the types
        searchQuery = client.factory.create('stationSearchRequest')
        # un-comment next line to see what parameters are supported
        #print searchQuery
        
        # add properties/filter options
        #searchQuery.Address = "80 S 2nd st"
        #searchQuery.City = "San Jose"
        #searchQuery.State = "CA"
        searchQuery.Proximity = nearby
        searchQuery.proximityUnit = 'M'
        # create goeData, provide starting point co-ordinates
        geoData = client.factory.create('geoData')
        # XXX we know what address to search for:
        # 442 N Canon Dr 
        # Beverly Hills, CA 90210
        geoData.Lat  = Glat
        geoData.Long = Glng
        searchQuery.Geo = geoData
		
        # here is the actual call to the service
        response = client.service.getPublicStations(searchQuery)
        #print response

        return response

	# do whatever with the data
	# print response
    except suds.WebFault as detail:
        print detail


#if __name__=="__main__":
    #main()
