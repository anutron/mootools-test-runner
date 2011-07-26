from django.conf.urls.defaults import *
import os

urlpatterns = patterns('frontend_dev',
    (r'^$', 'views.index'),
    (r'^(?P<version>.*)/bottom_frame/', 'views.bottom_frame'),
    (r'^(?P<version>.*)/top_nav/', 'views.top_nav'),
    (r'^welcome/', 'views.welcome'),

    (r'^depender/', include('depender.urls')),

    # Menus
    (r'^(?P<version>.*)/demo_menu/', 'views.demo_menu'),
    (r'^(?P<version>.*)/docs_menu/$', 'views.docs_menu'),
    (r'^(?P<version>.*)/docs_menu/(?P<project>(\w|-|_)+)/(?P<path>.*)$', 'views.docs_menu'),

    # Docs
    (r'^docs/(?P<project>(\w|-|_)+)/(?P<path>.*)$', 'views.docs'),
    (r'^(?P<version>.*)/viewdoc/(?P<path>.*)$', 'views.viewdoc'),
    (r'^toc/(?P<path>.*)$', 'views.toc'),
    (r'^(?P<version>.*)/source/', 'views.view_source'),
    # Demos
    (r'^(?P<version>.*)/demo/', 'views.demo'),
    (r'^^(?P<version>.*)/assets/(?P<path>.*)$', 'views.generic_asset'),
    (r'^assets/(?P<path>.*)$', 'views.generic_asset'),
    (r'^Source/(?P<path>.*)$', 'get_source_file'),
    (r'^get_source_file/(?P<project>(\w|-|_)+)/(?P<path>.*)$', 'views.get_source_file'),
    (r'^(?P<version>.*)/asset/(?P<project_name>(\w|-|_)+)/(?P<path>.*)$', 'views.asset'),
    (r'^asset/(?P<project_name>(\w|-|_)+)/(?P<path>.*)$', 'views.asset'),
    (r'^_assets/(?P<path>.*)$', 'asset'),


    # Specs & Benchmarks
    (r'^(?P<version>.*)/specs/', 'views.specs'),
    (r'^moorunner/(?P<path>.*)$', 'views.moorunner'),
    (r'^(?P<version>.*)/benchmarks/', 'views.specs', {'template':'benchmarks.mako'}),

    # Echo
    url(r'^echo/js/$','views.echo_js', name='echo_js'),
    url(r'^echo/json/$','views.echo_json', name='echo_json'),
    url(r'^echo/jsonp/$','views.echo_jsonp', name='echo_jsonp'),
    url(r'^echo/html/$','views.echo_html', name='echo_html'),
    url(r'^echo/xml/$','views.echo_xml', name='echo_xml'),

    # OLD ECHO
    url(r'^ajax_json_response/$','views.ajax_json_response', name='ajax_json_response'),
    url(r'^ajax_html_javascript_response/$','views.ajax_html_javascript_response', name='ajax_html_javascript_response'),
    url(r'^ajax_json_echo/$','views.ajax_json_echo', name='ajax_json_echo'),
    url(r'^ajax_json_echo/nodelay/$','views.ajax_json_echo', {'delay': False}, name='ajax_json_echo_nodelay'),
    url(r'^ajax_html_echo/$','views.ajax_html_echo', name='ajax_html_echo'),
    url(r'^ajax_html_echo/nodelay/$','views.ajax_html_echo', {'delay': False}, name='ajax_html_echo_nodelay'),
    url(r'^ajax_xml_echo/$','views.ajax_xml_echo', name='ajax_xml_echo'),
    url(r'^ajax_xml_echo/nodelay/$','views.ajax_xml_echo', {'delay': False}, name='ajax_xml_echo_nodelay'),
    
    # MooTools request.php implementation
    (r'^Helpers/request.php$', 'mootools_request_php.mootools_request_php'),

)
