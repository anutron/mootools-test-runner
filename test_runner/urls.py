from django.conf.urls.defaults import *
import os

urlpatterns = patterns('',
    (r'^$', 'test_runner.views.index'),
    (r'^test/', 'test_runner.views.test'),
    (r'^asset/(?P<project>\w+)/(?P<path>.*)$', 'test_runner.views.asset'),
    (r'^depender/', include('depender.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))}),
    (r'^ajax_json_response/$', 'test_runner.views.ajax_json_response'),
    (r'^ajax_html_javascript_response/$', 'test_runner.views.ajax_html_javascript_response'),
    (r'^ajax_json_echo/$', 'test_runner.views.ajax_json_echo'),
    (r'^ajax_html_echo/$', 'test_runner.views.ajax_html_echo'),
    (r'^ajax_xml_echo/$', 'test_runner.views.ajax_xml_echo_nodelay'),
)
