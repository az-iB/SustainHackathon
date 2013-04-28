# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext as RC
from search import searchDistanceWithMining

def home( request ):
    return render_to_response(
    'index.html',
    {},
    context_instance = RC( request, {} ),
    )

def search( request ):
    if 'textarea' in request.GET and request.GET['textarea']:
        print request.GET['textarea']

    return render_to_response(
    'index.html',
    )

def choices( request ):

    print '>>>>>>>>>'
    if 'location' in request.GET and request.GET['location']:
        location = request.GET['location']
        print 'User input: Location', location

    if 'datetime-3' in request.GET and request.GET['datetime-3']:
        dateTime = request.GET['datetime-3'][11:]
        print 'User input: datetime', dateTime
    else:
        dateTime = '02:00' # XXX

    choices = searchDistanceWithMining(request, dateTime)

    return render_to_response(
    'choices.html',
    {'choice_data': choices },
    context_instance = RC( request, {} ),
    )

def details( request ):
    if 'textarea' in request.GET and request.GET['textarea']:
        print request.GET['textarea']

    return render_to_response(
    'details.html',
    {},
    context_instance = RC( request, {} ),
    )

def notify( request ):
    if 'textarea' in request.GET and request.GET['textarea']:
        print request.GET['textarea']

    return render_to_response(
    'notify.html',
    {},
    context_instance = RC( request, {} ),
    )

def donetext( request ):

    # XXX register with our server for a text back when
    # the slot is occupied 15min before arriving
    # and recommend a new one

    return render_to_response(
    'done-text.html',
    {},
    context_instance = RC( request, {} ),
    )

def donecall( request ):
    if 'textarea' in request.GET and request.GET['textarea']:
        print request.GET['textarea']

    return render_to_response(
    'done-call.html',
    {},
    context_instance = RC( request, {} ),
    )

def donenone( request ):
    if 'textarea' in request.GET and request.GET['textarea']:
        print request.GET['textarea']

    return render_to_response(
    'done-none.html',
    {},
    context_instance = RC( request, {} ),
    )
