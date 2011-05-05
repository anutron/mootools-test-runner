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

excluded_tests = []
if hasattr(settings,'EXCLUDED_TESTS'):
  excluded_tests = settings.EXCLUDED_TESTS


def index(request):
  """ The main frameset. """
  return render_to_response('index.mako', 
    {
      'title': settings.TITLE_PREFIX
    }
  )

def welcome(request):
  """ The default 'home' page for the main content frame; pulls in WELCOME.md from the frontend_dev app. """
  welcome_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "WELCOME.md"))
  welcome = open(welcome_file, 'rb').read()
  return render_to_response('markdown.mako', 
    {
      'title': 'welcome',
      'title_prefix': settings.TITLE_PREFIX,
      'body': markdown(welcome)
    }
  )


# DEMOS
def demo(request):
  """ Given a project and path, renders the configured demo to the browser. """
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
  template = 'demo.mako'
  
  post_vars = None
  if request.POST: post_vars = request.POST.iteritems()
  if request.REQUEST.get('sleep'):
    sleep = int(request.REQUEST.get('sleep'))
    time.sleep(sleep)
  if re.search("mako$", full_path):
    request.path = request.META.get('PATH_INFO')
    if request.META.get('QUERY_STRING') and len(request.META.get('QUERY_STRING')) > 0:
      request.path += "?" + request.META.get('QUERY_STRING')
    def get_asset_url(project, path):
      return "/asset/" + project + "/" + path
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
      'current': make_demo_url(project, path),
      'projects': projects,
      'title_prefix': settings.TITLE_PREFIX,
      'previous': prev,
      'prev_name':prev_name,
      'next': next,
      'next_name':next_name,
      'excluded_tests': excluded_tests,
    }
  )


# SPECS
def specs(request, template="specs.mako"):
  """ Renders either a menu to choose tests or the runner with the selected tests. """
  specs = settings.MOOTOOLS_SPECS_AND_BENCHMARKS
  if request.GET.get('preset') is None:
    return render_to_response(template, {
          'title': settings.TITLE_PREFIX,
          'specs_packages': specs
        })
  else:
    presets = request.GET.getlist('preset')
    if 'all' not in presets:
      specs = presets
    return render_to_response(template, {
          'title': settings.TITLE_PREFIX,
          'specs': ','.join(specs)
        })

def moorunner(request, path):
  """ Returns an asset from the MooTools Jasmine test runner. """
  return read_asset(os.path.normpath(settings.MOOTOOLS_RUNNER_PATH + '/' + path))


# VIEW SOURCE
def view_source(request):
  """ Returns the contents of a given project/path combination in the view-source viewer. Reads
      yaml files that configure addtional sources to include in the view. """
  def format_code(extension, code_str):
    """Fix indent and highlight code"""
    try:
      lexer = get_lexer_by_name('html', tabsize=2)
      return highlight(code_str, lexer, HtmlFormatter())
    except KeyError:
      LOG.warn('Cannot find lexer for extension %s' % (extension,))
      return "<div><pre>%s</pre></div>" % (code_str,)
  
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
      'current': make_demo_url(project, path),
      'projects': projects,
      'title_prefix': settings.TITLE_PREFIX,
    }
  )


# DOCS
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


#  NAVIGATION
def top_nav(request):
  """ Renders the top navigation frame. """
  return render_to_response('top_nav.mako', {
    'title': settings.TITLE_PREFIX,
    'show_docs': True,
    'show_demos': True,
    'show_specs': True,
    'show_benchmarks': True,
  })

def bottom_frame(request):
  """ Given a url for the menu_path and content_path renders the bottom frames. """
  menu = request.REQUEST.get('menu_path')
  content = request.REQUEST.get('content_path')
  return render_to_response('bottom_frame.mako', {
    'title': settings.TITLE_PREFIX,
    'menu': menu,
    'content': content
  })

def test_menu(request):
  """ Renders a menu with a list of all available tests. """
  projects, dir_map = get_files(settings.MOOTOOLS_TEST_LOCATIONS, HTML_MATCHER, url_maker=make_demo_url)
  return render_to_response('left_menu.mako', 
    {
      'projects': projects,
      'title': 'Demos',
      'excluded_tests': excluded_tests
    }
  )
def docs_menu(request):
  """ Renders a menu with a list of all available docs. """
  projects, dir_map = get_docs_files()
  return render_to_response('left_menu.mako', 
    {
      'projects': projects,
      'title': 'Docs',
    }
  )



# ASSETS
def get_source_file(request, project, path):
  """ Given a project returns the contents of a file in its /Source directory. """
  if '..' in path:
    raise Exception("The path %s is invalid." % path)
  full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", project, "Source", path))
  return read_asset(full_path)

def asset(request, project, path):
  """ Given a project returns a file located in the test configuration path inside a subdirecotry called _assets. """
  project_dir = settings.MOOTOOLS_TEST_LOCATIONS[project]
  if '..' in path:
    raise Exception("The path %s is invalid." % path)
  full_path = os.path.normpath(project_dir + "/_assets/" + path)
  return read_asset(full_path)

def assets(request, project, path):
  """ Deprecated """
  return asset(request, project, path)

def generic_asset(request, path):
  """ A wrapper for generic paths. Reads configuration values from settings for any path and 
      returns the configured path's contents instead. This is useful when you are running specs
      from a 3rd party (MooTools Core, for example) that expects certain files to be in a specific place. """
  if hasattr(settings,'GENERIC_ASSETS') and settings.GENERIC_ASSETS[path] is not None:
    return read_asset(os.path.normpath(settings.GENERIC_ASSETS[path]))
  else:
    raise Exception("The asset for %s was not found." % path)

def read_asset(path):
  """ Given a path, reads the contents of that file and returns it with the proper mime type. """
  if not os.path.isfile(path):
    raise Exception("The file %s was not found." % path)
  data = open(path, "rb").read()
  
  content_types = {
    "html": "text/html",
    "xml": "text/xml",
    "csv": "text/csv",
    "png": "image/png",
    "jpg": "image/jpg",
    "gif": "image/gif",
    "css": "text/css",
    "less": "text/less",
    "js": "application/x-javascript",
    "flv": "video/x-flv",
    "swf": "application/x-shockwave-flash"
  }
  for extension, content_type in content_types.iteritems():
    if re.search(extension + "$(?i)", path):
      return HttpResponse(data, mimetype = content_type)
  
  raise Exception("Unknown asset type (currently only html/png/gif/jpg/css/js are supported).")


# ECHOS
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

def ajax_json_echo(req, delay=False):
    " OLD: echo GET and POST via JSON "
    if delay:
        time.sleep(random.uniform(1,3))
    c = {'get_response':{},'post_response':{}}
    for key, value in req.GET.items():
        c['get_response'].update({key: value})
    for key, value in req.POST.items():
        c['post_response'].update({key: value})
    return HttpResponse(simplejson.dumps(c),mimetype='application/javascript')

def ajax_html_echo(req, delay=False):
    " OLD: echo POST['html'] "
    if delay:
        time.sleep(random.uniform(1,3))
    t = req.POST.get('html','')
    return HttpResponse(t)

def ajax_xml_echo(req, delay=False):
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


# FILE CRAWLERS
def get_files_by_project(project, directory, matcher, url_maker, dirs = None, file_map = None, include_root = None):
  """ Given a project and a direcotry, returns all files in that directory that match the specified 'matcher' regular expression. """
  if dirs is None:
    dirs = {}
  if file_map is None:
    file_map = {}
  def get_file_dict(files, directory):
    return dict([(url_maker(project, file.replace(directory, '')), make_title(file.split('/')[-1])) for file in files])
  
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
  
  if include_root is not None:
    match_files(directory + include_root, recurse=False)
  match_files(directory)
  return dirs, file_map
  

def get_files(locations, matcher, url_maker):
  """ Given a dict of locations, finds all files in those locations that match the specified 'matcher' regular expression.  """
  dirs = {}
  file_map = {}
  
  for project, directory in locations.iteritems():
    get_files_by_project(project, directory, matcher, url_maker, dirs, file_map, include_root = "/..")
    
  return dirs, file_map

def get_test_files(project = None):
  """ Given a specified project, return all the HTML files in that configured path from the settings.
      If no project is specified, returns all HTML files in all the configured test directories."""
  if project:
    return get_files_by_project(project, settings.MOOTOOLS_TEST_LOCATIONS[project],
      matcher=HTML_MATCHER, url_maker=make_demo_url)
  return get_files(locations=settings.MOOTOOLS_TEST_LOCATIONS, matcher=HTML_MATCHER, url_maker=make_demo_url)

def get_docs_files(project=None):
  """ Gets all markdown documents in a specified project or, if none is specified, all the markdown
      files in all the specified docs directories from the settings. """
  if project:
    return get_files_by_project(project, settings.DOCS[project],
      matcher=MARKDOWN_MATCHER, url_maker=docs_url)
  return get_files(locations=settings.DOCS, matcher=MARKDOWN_MATCHER, url_maker=docs_url)

def get_js_in_dir_tree(directory):
  """ Given a path to a directory, finds all JavaScript files.
      Does not appear to be used? """
  js = []
  for root, subdirs, files in os.walk(directory):
    js.extend([os.path.join(directory, name) for name in os.listdir(os.path.join(directory)) if JS_MATCHER.search(name)])
    for subdir in subdirs:
      js.extend(get_js_in_dir_tree(os.path.join(directory, subdir)))
  return js


# URL & TITLE MAKERS
def make_demo_url(project, path):
  """ Given a path and a project, returns a url for the demo."""
  return '/demo/?project='+quote(project)+'&path='+path

def make_title(path):
  """ Given a path, return a suiteable title for the file name."""
  return re.sub('[\._]', ' ', re.sub('(\.(html|mako|md|markdown))', '', path))

def docs_url(project, path):
  """ Given a project and a path, return the url for the docs. """
  root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
  project_path = settings.DOCS[project]
  docs_path = project_path.replace(root, '')
  return os.path.normpath('/docs/' + docs_path + path);



