from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
                           (r'^$', 'codeoff.pythonoff.views.index.index'),
                           (r'^ajax/send_buffer/', 'codeoff.pythonoff.views.ajax.send_buffer'),
                           (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root':'/Users/jacob/programming/CodeOff/codeoff/resources'}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
