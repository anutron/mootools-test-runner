from django.conf.urls.defaults import *
import os

urlpatterns = patterns('test_runner.views',
    (r'^$', 'index'),
    (r'^test/', 'test'),
    (r'^asset/(?P<project>\w+)/(?P<path>.*)$', 'asset'),
    (r'^depender/', include('depender.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))}),
    # Echo
    url(r'^echo/js/$','echo_js', name='echo_js'),
    url(r'^echo/json/$','echo_json', name='echo_json'),
    url(r'^echo/jsonp/$','echo_jsonp', name='echo_jsonp'),
    url(r'^echo/html/$','echo_html', name='echo_html'),
    url(r'^echo/xml/$','echo_xml', name='echo_xml'),

    # OLD ECHO
    url(r'^ajax_json_response/$','ajax_json_response', name='ajax_json_response'),
    url(r'^ajax_html_javascript_response/$','ajax_html_javascript_response', name='ajax_html_javascript_response'),
    url(r'^ajax_json_echo/$','ajax_json_echo', name='ajax_json_echo'),
    url(r'^ajax_json_echo/nodelay/$','ajax_json_echo', {'delay': False}, name='ajax_json_echo_nodelay'),
    url(r'^ajax_html_echo/$','ajax_html_echo', name='ajax_html_echo'),
    url(r'^ajax_html_echo/nodelay/$','ajax_html_echo', {'delay': False}, name='ajax_html_echo_nodelay'),
    url(r'^ajax_xml_echo/$','ajax_xml_echo', name='ajax_xml_echo'),
    url(r'^ajax_xml_echo/nodelay/$','ajax_xml_echo', {'delay': False}, name='ajax_xml_echo_nodelay'),
)
