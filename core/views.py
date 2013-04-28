# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext as RC

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
    {},
    context_instance = RC( request, {} ),
    )

def choices( request ):
    if 'textarea' in request.GET and request.GET['textarea']:
        print request.GET['textarea']

    return render_to_response(
    'choices.html',
    {},
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
    if 'textarea' in request.GET and request.GET['textarea']:
        print request.GET['textarea']

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
