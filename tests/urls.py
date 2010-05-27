from django.conf.urls.defaults import *
import os

urlpatterns = patterns('',
    (r'^$', 'tests.views.index'),
    (r'^test/(.+)', 'tests.views.test'),
    (r'^depender/', include('depender.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))}),
)
