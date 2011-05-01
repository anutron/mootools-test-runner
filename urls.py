from django.conf.urls.defaults import *
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^frontend_dev/', include('frontend_dev.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^', include('frontend_dev.urls')), 
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))}),
    
)
