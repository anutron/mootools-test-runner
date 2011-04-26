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
from django.http import HttpResponse, HttpResponseRedirect
from markdown import markdown
from urllib import quote

from depender.views import depender as dep
from pygments import highlight
from pygments.filters import NameHighlightFilter
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.token import Name
import yaml


HTML_MATCHER = re.compile("\.(html|mako)$")
MARKDOWN_MATCHER = re.compile("\.(markdown|md)$")
JS_MATCHER = re.compile("\.(js)$")


def index(request):
  projects, dir_map = get_files(settings.MOOTOOLS_TEST_LOCATIONS, HTML_MATCHER, url_maker=make_url)
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

def specs(request):
  specs = settings.MOOTOOLS_SPECS_AND_BENCHMARKS
  if request.GET.get('preset') is None:
    return render_to_response('choose_specs.mako', {
          'title': settings.TITLE_PREFIX,
          'specs_packages': specs
        })
  else:
    presets = request.GET.getlist('preset')
    if 'all' not in presets:
      specs = presets
    return render_to_response('specs.mako', {
          'title': settings.TITLE_PREFIX,
          'specs_packages': ','.join(specs)
        })

def moorunner(request, path):
  return read_asset(os.path.normpath(settings.MOOTOOLS_RUNNER_PATH + '/' + path))

def asset(request, project, path):
  project_dir = settings.MOOTOOLS_TEST_LOCATIONS[project]
  if '..' in path:
    raise Exception("The path %s is invalid." % path)
  full_path = os.path.normpath(project_dir + "/_assets/" + path)
  return read_asset(full_path)

def assets(request, project, path):
  return asset(request, project, path)

def generic_asset(request, path):
  if hasattr(settings,'GENERIC_ASSETS') and settings.GENERIC_ASSETS[path] is not None:
    return read_asset(os.path.normpath(settings.GENERIC_ASSETS[path]))
  else:
    raise Exception("The asset for %s was not found." % path)

def read_asset(path):
  if not os.path.isfile(path):
    raise Exception("The file %s was not found." % path)
  data = open(path, "rb").read()
  
  content_types = {
    "html": "text/html",
    "png": "image/png",
    "jpg": "image/jpg",
    "gif": "image/gif",
    "css": "text/css",
    "js": "application/x-javascript",
    "flv": "video/x-flv",
    "swf": "application/x-shockwave-flash"
  }
  for extension, content_type in content_types.iteritems():
    if re.search(extension + "$(?i)", path):
      return HttpResponse(data, mimetype = content_type)
  
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

  projects, dir_map = get_test_files()
  project_dir = settings.MOOTOOLS_TEST_LOCATIONS[project]
  full_path = os.path.normpath(project_dir+path)

  file_path, extension = os.path.splitext(path)
  try:
    data = format_code(extension[1:], file(full_path).read())
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
          js_data[ref] = format_code('js', file_data.content)
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


def format_code(extension, code_str):
  """Fix indent and highlight code"""
  try:
    lexer = get_lexer_by_name('html', tabsize=2)
    return highlight(code_str, lexer, HtmlFormatter())
  except KeyError:
    LOG.warn('Cannot find lexer for extension %s' % (extension,))
    return "<div><pre>%s</pre></div>" % (code_str,)


def test(request):
  project = request.REQUEST.get('project')
  path = request.REQUEST.get('path')
  sleeper(request)
  if project is None or path is None:
    raise Exception("You must specify a project and a path.")
  
  projects, dir_map = get_test_files()
  
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

def get_url(test):
  project_dir = settings.MOOTOOLS_TEST_LOCATIONS[test['project']]
  path = test['filename'].replace(project_dir, '')
  return make_url(path, test['project'])

def get_files_by_project(project, directory, matcher, url_maker, dirs = None, file_map = None):
  if dirs is None:
    dirs = {}
  if file_map is None:
    file_map = {}
  def get_file_dict(files, directory):
    return dict([(url_maker(file.replace(directory, ''), project), make_title(file.split('/')[-1])) for file in files])

  def match_files(current_dir, recurse=True):
    matching_files = []
    for entry in os.listdir(current_dir):
      if entry != "_assets":
        path = os.path.join(current_dir, entry)
        if os.path.isdir(path):
          if recurse:
            match_files(path, recurse)
        elif matcher.search(entry):
          matching_files.append(path)
          file_map[path] = dict(
            project = project_title,
            subdir = current_dir,
            filename = path
          )
    
    if len(matching_files) > 0:
      dirs[project_title].append(dict(
        subdir = current_dir,
        title = make_title(current_dir.split('/')[-1]),
        files = matching_files,
        file_dict = get_file_dict(matching_files, directory)
      ))
  
  project_title = make_title(project)
  dirs[project_title] = []
  
  match_files('.', recurse=False)
  match_files(directory)
  return dirs, file_map
  

def get_files(locations, matcher, url_maker):
  dirs = {}
  file_map = {}
  
  for project, directory in locations.iteritems():
    get_files_by_project(project, directory, matcher, url_maker, dirs, file_map)
    
  return dirs, file_map

def get_test_files(project = None):
  if project:
    return get_files_by_project(project, settings.MOOTOOLS_TEST_LOCATIONS[project],
      matcher=HTML_MATCHER, url_maker=make_url)
  return get_files(locations=settings.MOOTOOLS_TEST_LOCATIONS, matcher=HTML_MATCHER, url_maker=make_url)

def get_docs_files(project):
  if project:
    return get_files_by_project(project, settings.DOCS[project],
      matcher=MARKDOWN_MATCHER, url_maker=docs_url)
  get_files(locations=settings.DOCS, matcher=MARKDOWN_MATCHER, url_maker=docs_url)

def get_js_in_dir_tree(directory):
  js = []
  for root, subdirs, files in os.walk(directory):
    js.extend([os.path.join(directory, name) for name in os.listdir(os.path.join(directory)) if JS_MATCHER.search(name)])
    for subdir in subdirs:
      js.extend(get_js_in_dir_tree(os.path.join(directory, subdir)))
  return js

def make_url(path, project):
  return '/test/?project='+quote(project)+'&path='+path

def make_title(path):
  return re.sub('[\._]', ' ', re.sub('(\.(html|mako|md|markdown))', '', path))

def docs_url(path, project):
  root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
  project_path = settings.DOCS[project]
  docs_path = project_path.replace(root, '')
  return os.path.normpath('/docs/' + docs_path + path);

def docs(request, path):
  if path == '':
    path = "test-runner/WELCOME"
  if not re.search("md$(?i)", path):
    path = path + '.md'
  text = None
  if '..' in path:
    raise Exception('invalid path: %s' % path)
  else:
    md = os.path.abspath(os.path.join(settings.DOC_ROOT, path))
    if os.path.isfile(md):
      text = open(md, 'rb').read()
  if text is None:
    raise Exception("The path %s was not found." % path)
  else:
    parsed = markdown(text)
    dirs, files = get_docs_files()
    
    toc = []
    
    def replacer(matchobj):
      match = matchobj.group(0)
      match = re.sub('\{#|}', '', match)
      toc.append(match)
      return '<a class="toc_anchor" name="' + match + '"></a><a href="#top" class="to_top">back to top</a>'
      
    parsed = re.sub("\{#.*?}", replacer, parsed)
    
    return render_to_response('markdown.mako', 
      {
        'body': parsed,
        'docs': files,
        'title': make_title(path.split('/')[-1]),
        'title_prefix': settings.TITLE_PREFIX,
        'current': 'docs/' + path,
        'dirs': dirs,
        'toc': toc
      }
    )
    
