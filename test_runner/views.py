# Create your views here.

from djangomako.shortcuts import render_to_response, render_to_string
import os
import re
import time
import simplejson
import random
import mako
from mako.template import Template
from django.conf import settings
from django.http import HttpResponse
from markdown import markdown
from urllib import quote

from depender.views import depender as dep
from pygments import highlight
from pygments.filters import NameHighlightFilter
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.token import Name
import yaml



def index(request):
  projects, dir_map = get_files()
  welcome_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "WELCOME.md"))
  welcome = open(welcome_file, 'rb').read()
  return render_to_response('index.mako', 
    {
      'welcome': markdown(welcome),
      'projects': projects,
      'title_prefix': settings.TITLE_PREFIX,
      'current': None,
      'next': None,
      'previous': None,
      'excluded_tests': get_excluded_tests()
    }
  )

def choose_specs(request):
  specs = settings.MOOTOOLS_SPECS_AND_BENCHMARKS
  return render_to_response('choose_specs.mako', {
        'title': settings.TITLE_PREFIX,
        'specs_packages': specs
      })

def run_specs(request):
  specs = request.GET.getlist('preset')
  return render_to_response('specs.mako', {
        'title': settings.TITLE_PREFIX,
        'specs_packages': ','.join(specs)
      })
def moorunner(request, path):
  return read_asset(os.path.normpath(settings.MOOTOOLS_RUNNER_PATH + '/' + path))

def asset(request, project, path):
  project_dir = settings.MOOTOOLS_TEST_LOCATIONS[project]
  full_path = os.path.normpath(project_dir + "/_assets/" + path)
  return read_asset(path)

def generic_asset(request, path):
  if hasattr(settings,'GENERIC_ASSETS') and settings.GENERIC_ASSETS[path] is not None:
    return read_asset(os.path.normpath(settings.GENERIC_ASSETS[path]))
  else:
    raise Exception

def read_asset(path):
  if not os.path.isfile(path):
    raise Exception("The path %s was not found." % path)
  data = open(path, "rb").read()
  if re.search("html$(?i)", path):
    return HttpResponse(data, mimetype="text/html")
  if re.search("png$(?i)", path):
    return HttpResponse(data, mimetype="image/png")
  if re.search("jpg$(?i)", path):
    return HttpResponse(data, mimetype="image/jpg")
  if re.search("gif$(?i)", path):
    return HttpResponse(data, mimetype="image/gif")
  if re.search("css$(?i)", path):
    return HttpResponse(data, mimetype="text/css")
  if re.search("js$(?i)", path):
    return HttpResponse(data, mimetype="application/x-javascript")
  if re.search("flv$(?i)", path):
    return HttpResponse(data, mimetype="video/x-flv")
  if re.search("swf$(?i)", path):
    return HttpResponse(data, mimetype="application/x-shockwave-flash")
  raise Exception("Unknown asset type (currently only html/png/gif/jpg/css/js are supported).")


def mootools_request_php(req):
  content_types = {
    'text': 'text/plain',
    'html': 'text/html',
    'xml': 'application/xml',
    'json': 'application/json',
    'script': 'application/javascript',
    'javascript': 'application/javascript'
  }
  sleep = req.REQUEST.get('__sleep')
  response = req.REQUEST.get('__response')
  reqtype = req.REQUEST.get('__type', 'html')
  retrieve = req.REQUEST.get('__retrieve')
  if sleep is not None:
    time.sleep(float(sleep))

  if response is not None:
    return HttpResponse(response, mimetype=content_types[reqtype])
  elif retrieve is not None:
    response = simplejson.dumps(simplejson.loads(retrieve))
    return HttpResponse(response, mimetype=content_types[reqtype])
  else:
    obj = {
      'method': req.META['REQUEST_METHOD'].lower()
    }
    if obj['method'] == 'get':
      obj['get'] = simplejson.loads(simplejson.dumps(req.GET))
    elif obj['method'] == 'post':
      obj['post'] = simplejson.loads(simplejson.dumps(req.POST))
    response = simplejson.dumps(obj)
    return HttpResponse(response, mimetype=content_types[reqtype])

# the following ajax responses borrowed from MooShell - thx Piotr!
def echo_js(req):
    " respond JS from GET/POST['js']"
    sleeper(req)
    return HttpResponse(req.REQUEST.get('js', ''),
                      mimetype='application/javascript')


def echo_json(req):
    " respond with GET/POST['json'] "
    sleeper(req)
    try:
        response = simplejson.dumps(
            simplejson.loads(req.REQUEST.get('json', '{}')))
    except Exception, e:
        response = simplejson.dumps({'error': str(e)})

    return HttpResponse(
        response,
        mimetype='application/javascript'
    )


def echo_html(req):
    " respond with GET/POST['html'] "
    sleeper(req)
    return HttpResponse(req.REQUEST.get('html', ''))


def echo_jsonp(req):
    " respond what provided via GET/POST "
    sleeper(req)
    response = {}
    callback = req.REQUEST.get('callback', False)
    noresponse_keys = ['callback', 'delay']

    for key, value in req.REQUEST.items():
        if key not in noresponse_keys:
            response.update({key: value})

    response = simplejson.dumps(response)

    if callback:
        response = '%s(%s);' % (callback, response)

    return HttpResponse(response, mimetype='application/javascript')


def echo_xml(req):
    " respond with GET/POST['xml'] "
    sleeper(req)
    return HttpResponse(req.REQUEST.get('xml', ''), mimetype='text/xml')

def sleeper(req):
  if req.REQUEST.get('delay'):
      time.sleep(float(req.REQUEST.get('delay')))
  if req.REQUEST.get('sleep'):
      time.sleep(float(req.REQUEST.get('sleep')))

def ajax_json_echo(req, delay=True):
    " OLD: echo GET and POST via JSON "
    if delay:
        time.sleep(random.uniform(1,3))
    c = {'get_response':{},'post_response':{}}
    for key, value in req.GET.items():
        c['get_response'].update({key: value})
    for key, value in req.POST.items():
        c['post_response'].update({key: value})
    return HttpResponse(simplejson.dumps(c),mimetype='application/javascript')


def ajax_html_echo(req, delay=True):
    " OLD: echo POST['html'] "
    if delay:
        time.sleep(random.uniform(1,3))
    t = req.POST.get('html','')
    return HttpResponse(t)


def ajax_xml_echo(req, delay=True):
    " OLD: echo POST['xml'] "
    if delay:
        time.sleep(random.uniform(1,3))
    t = req.POST.get('xml','')
    return HttpResponse(t, mimetype='application/xml')


def ajax_json_response(req):
    " OLD: standard JSON response "
    response_string = req.POST.get('response_string','This is a sample string')
    return HttpResponse(simplejson.dumps(
        {
            'string': response_string,
            'array': ['This','is',['an','array'],1,2,3],
            'object': {'key': 'value'}
        }),
        mimetype='application/javascript'
    )


def ajax_html_javascript_response(req):
    return HttpResponse("""<p>A sample paragraph</p>
<script type='text/javascript'>alert('sample alert');</script>""")

def view_source(request):
  project = request.REQUEST.get('project')
  path = request.REQUEST.get('path')
  if project is None or path is None:
    raise Exception("You must specify a project and a path.")

  projects, dir_map = get_files()
  project_dir = settings.MOOTOOLS_TEST_LOCATIONS[project]
  full_path = os.path.normpath(project_dir+path)

  file_path, extension = os.path.splitext(path)
  try:
    data = format_code(extension, file(full_path).read())
  except OSError, ex:
    raise Exception("Cannot read requested gallery template: %s" % (path,))




  # Load the js references
  js_data = { }         # map of { name: js content }
  yml_file = os.path.splitext(full_path)[0] + '.yml'
  if os.path.exists(yml_file):
    yml = yaml.load(file(yml_file))
    try:
      for ref in yml['js-references']:
        try:
          js_pkg, js_comp = ref.split('/')
        except ValueError:
          raise Exception('Invalid line "%s" in file %s' % (ref, yml_file))
        try:
          file_data = dep.get((js_pkg, js_comp))
          js_data[ref] = format_code('.js', file_data.content)
        except:
          raise Exception(
            'Cannot locate "%s" package "%s" component' % (js_pkg, js_comp))
    except KeyError, ex:
      LOG.warn('%s does not have a "js-references" section' % (yml_file,))

  return render_to_response('view_source.mako',
      {
      'data': data,
      'js_data': js_data,
      'title': make_title(path.split('/')[-1]),
      'current': make_url(path, project),
      'projects': projects,
      'title_prefix': settings.TITLE_PREFIX,
    }
  )

_LEXER_MAP = {
  '.html': get_lexer_by_name('html', tabsize=2),
  '.js': get_lexer_by_name('js', tabsize=2),
  '.mako': get_lexer_by_name('mako', tabsize=2),
}


def format_code(extension, code_str):
  """Fix indent and highlight code"""
  try:
    lexer = _LEXER_MAP[extension]
    return highlight(code_str, lexer, HtmlFormatter())
  except KeyError:
    LOG.warn('Cannot find lexer for extension %s' % (extension,))
    return "<div><pre>%s</pre></div>" % (code_str,)


def test(request):
  projects, dir_map = get_files()
  project = request.REQUEST.get('project')
  path = request.REQUEST.get('path')
  sleeper(request)
  if project is None or path is None:
    raise Exception("You must specify a project and a path.")
  
  project_dir = settings.MOOTOOLS_TEST_LOCATIONS[project]
  full_path = os.path.normpath(project_dir+path)

  dir_keys = dir_map.keys()
  try:
    current_index = dir_keys.index(full_path)
  except:
    raise Exception("The path %s was not found." % path)

  prev = None
  next = None
  found = False
  for proj, directories in sorted(projects.items()):
    if next is not None:
      break
    for directory in sorted(directories):
      if next is not None:
        break
      for file_path, file_title in sorted(directory['file_dict'].items()):
        if next is not None:
          break
        if found:
          next = file_path
        if str(file_path.split('path=')[-1]) == str(path):
          found = True
        if not found:
          prev = file_path

  if prev:
    prev_name = make_title(prev.split('/')[-1])
  else:
    prev_name = None
  if next:
    next_name = make_title(next.split('/')[-1])
  else:
    next_name = None


  test_source = open(full_path).read()
  template = 'test.mako'
  
  post_vars = None
  if request.POST: post_vars = request.POST.iteritems()
  if request.REQUEST.get('sleep'):
    sleep = int(request.REQUEST.get('sleep'))
    time.sleep(sleep)
  if re.search("mako$", full_path):
    request.path = request.META.get('PATH_INFO')
    if request.META.get('QUERY_STRING') and len(request.META.get('QUERY_STRING')) > 0:
      request.path += "?" + request.META.get('QUERY_STRING')
    source = Template(test_source).render(
      post_vars = post_vars,
      get_var = request.REQUEST.get,
      get_list = request.REQUEST.getlist,
      request_path = request.path,
      get_request = lambda: request,
      get_asset_url = get_asset_url
    )
  else:
    source = test_source
  if 'test_runner_no_wrapper' in source or request.REQUEST.get('no_wrapper') == 'true':
    template = 'blank.mako'
  
  return render_to_response(template,
      {
      'test': source,
      'title': make_title(path.split('/')[-1]),
      'current': make_url(path, project),
      'projects': projects,
      'title_prefix': settings.TITLE_PREFIX,
      'previous': prev,
      'prev_name':prev_name,
      'next': next,
      'next_name':next_name,
      'excluded_tests': get_excluded_tests(),
    }
  )

def get_asset_url(project, path):
  return "/asset/" + project + "/" + path


def get_excluded_tests():
  excluded_tests = []
  if hasattr(settings,'EXCLUDED_TESTS'):
    excluded_tests = settings.EXCLUDED_TESTS
  return excluded_tests

HTML_MATCHER = re.compile("\.(html|mako)$")
JS_MATCHER = re.compile("\.(js)$")

def get_url(test):
  project_dir = settings.MOOTOOLS_TEST_LOCATIONS[test['project']]
  path = test['filename'].replace(project_dir, '')
  return make_url(path, test['project'])

def get_files():
  dirs = dict()
  file_map = dict()
  for project, directory in settings.MOOTOOLS_TEST_LOCATIONS.iteritems():
    files = []
    project_as_title = make_title(project)
    dirs[project_as_title] = []
    for root, subdirs, files in os.walk(directory):
      for subdir in subdirs:
        if subdir != "_assets":
          testfiles = [os.path.join(directory, subdir, name) for name in os.listdir(os.path.join(directory, subdir)) if HTML_MATCHER.search(name)]
          dirs[project_as_title].append(dict(
            subdir=make_title(subdir),
            files=testfiles,
            file_dict=get_file_dict(testfiles, directory, project)
          ))
          for filename in testfiles:
            file_map[filename] = dict(
              project=project_as_title,
              subdir=subdir,
              filename=filename
            )
  return dirs, file_map

def get_js_in_dir_tree(directory):
  js = []
  for root, subdirs, files in os.walk(directory):
    js.extend([os.path.join(directory, name) for name in os.listdir(os.path.join(directory)) if JS_MATCHER.search(name)])
    for subdir in subdirs:
      js.extend(get_js_in_dir_tree(os.path.join(directory, subdir)))
  return js

def get_file_dict(files, directory, project):
  return dict([(make_url(file.replace(directory, ''), project), make_title(file.split('/')[-1])) for file in files])

def make_url(path, project):
  return '?project='+quote(project)+'&path='+path

def make_title(path):
  return re.sub('(\.|_)', ' ', re.sub('(\.(html|mako))', '', path))