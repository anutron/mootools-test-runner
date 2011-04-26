from django.conf.urls.defaults import *
import os

urlpatterns = patterns('test_runner.views',
    (r'^$', 'index'),
    (r'^test/', 'test'),
    (r'^specs/', 'specs'),
    (r'^moorunner/(?P<path>.*)$', 'moorunner'),
    (r'^Helpers/request.php$', 'mootools_request_php'),
    (r'^assets/(?P<path>.*)$', 'generic_asset'),
    (r'^source/', 'view_source'),
    (r'^docs/(?P<path>.*)$', 'docs'),
    (r'^get_source_file/(?P<project>(\w|-|_)+)/(?P<path>.*)$', 'get_source_file'),
    (r'^asset/(?P<project>(\w|-|_)+)/(?P<path>.*)$', 'asset'),
    (r'^depender/', include('depender.urls')),

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
