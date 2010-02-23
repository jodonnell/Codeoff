from django.conf.urls.defaults import *

from codeoff.pythonoff.conf import local_settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
                       (r'^$', 'codeoff.pythonoff.views.index.index'),

                       (r'^ajax/update/$', 'codeoff.pythonoff.views.ajax.update'),
                       (r'^ajax/find_challenger/$', 'codeoff.pythonoff.views.ajax.find_challenger'),
                       (r'^ajax/run_program/$', 'codeoff.pythonoff.views.ajax.run_program'),

                       (r'^accounts/create/$', 'codeoff.pythonoff.views.users.create_user'),
                       (r'^accounts/login/$', 'codeoff.pythonoff.views.users.codeoff_login'),
                       (r'^accounts/logout/$', 'codeoff.pythonoff.views.users.codeoff_logout'),

                       (r'^resources/(?P<path>.*)$', 'django.views.static.serve', {'document_root':local_settings.MEDIA_ROOT}),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
