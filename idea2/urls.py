from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'core.views.home', name='home'),
    #url(r'^login/', 'core.views.login', name='login'),

    url(r'^login/$','django.contrib.auth.views.login',
        dict(
            template_name = 'login.html',
        ),
        name='login',
    ),

    url(
    r'^logout/$','django.contrib.auth.views.logout',
        dict(
            template_name = 'logout.html',
        ),
        name='logout',
    ),

    url(r'^search/','core.views.search'),

    url(r'^choices/','core.views.choices'),
    
    url(r'^details/','core.views.details'),

    url(r'^notify/','core.views.notify'),  

    url(r'^donetext','core.views.donetext'),  
    
    url(r'^donecall','core.views.donecall'),  
    
    url(r'^donenone','core.views.donenone'),  
    #(r'^accounts/', include('registration.urls')),

    # url(r'^idea2/', include('idea2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
