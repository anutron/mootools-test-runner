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

from depender.views import get_depender
from pygments import highlight
from pygments.filters import NameHighlightFilter
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.token import Name
import yaml

import logging
LOG = logging.getLogger(__name__)

get_path = settings.GET_PATH

HTML_MATCHER = re.compile("\.(html|mako)$")
MARKDOWN_MATCHER = re.compile("\.(markdown|md)$")
JS_MATCHER = re.compile("\.(js)$")
COMMENT_BLOCK = re.compile("\/\*.*\*\/", re.MULTILINE | re.DOTALL)

def get_version(request):
  return request.GET.get('version', settings.DEFAULT_VERSION)

def get_version_settings(version=None):
  if version is None:
    version = settings.DEFAULT_VERSION
  return settings.PROJECTS[version]

def index(request, path=False, content_path=False):
  """ The main frameset. """

  version = get_version(request)

  if content_path is False:
    content_path = '/welcome'
  if path is False:
    path = request.REQUEST.get('bottom', '/' + version + '/bottom_frame?menu_path=/' + version + '/docs_menu&content_path=' + content_path)

  return render_to_response('index.mako',
    {
      'title': settings.TITLE_PREFIX,
      'bottom': path,
      'version': version
    }
  )

def docs(request, project, path):
  return index(request, path = '/bottom_frame?menu_path=/docs_menu/' + project + '/' + path + '&content_path=/viewdoc/' + project + '/Docs/' + path)

def welcome(request):
  """ The default 'home' page for the main content frame; pulls in WELCOME.md from the frontend_dev app. """
  welcome = open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "WELCOME.md")), 'rb').read()
  return render_to_response('markdown.mako',
    {
      'title': 'welcome',
      'title_prefix': settings.TITLE_PREFIX,
      'body': markdown(welcome)
    }
  )


# DEMOS
def demo(request, version):
  """ Given a project and path, renders the configured demo to the browser. """
  project_name = request.REQUEST.get('project')
  path = request.REQUEST.get('path')
  sleeper(request)
  if project_name is None or path is None:
    raise Exception("You must specify a project and a path.")

  projects, dir_map = get_test_files(version)

  project = _get_project(version, project_name)
  full_path = os.path.normpath(get_path(project['demos']['path'])+path)

  dir_keys = dir_map.keys()

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
    def get_asset_url(project, path, version=None):
      if version is None:
        version = settings.DEFAULT_VERSION
      return "/" + version + "/asset/" + project + "/" + path
    source = Template(test_source).render(
      post_vars = post_vars,
      get_var = request.REQUEST.get,
      get_list = request.REQUEST.getlist,
      request_path = request.path,
      get_request = lambda: request,
      get_asset_url = get_asset_url,
      version = version
    )
  else:
    source = test_source
  if 'test_runner_no_wrapper' in source or request.REQUEST.get('no_wrapper') == 'true':
    template = 'blank.mako'

  return render_to_response(template,
    {
      'test': source,
      'title': make_title(path.split('/')[-1]),
      'current': make_demo_url(version, project_name, path),
      'projects': projects,
      'title_prefix': settings.TITLE_PREFIX,
      'version': version
    }
  )


# SPECS
def specs(request, version=None, template="specs.mako"):
  """ Renders either a menu to choose tests or the runner with the selected tests. """
  presets = request.GET.getlist('preset')
  if len(presets) == 0 or 'all' in presets:
    specs = _get_all_specs_packages(version)
    specs_names = []
    for spec in specs:
      spec_data = _read_yaml(get_path(spec))
      specs_names.append(spec_data['name'])

    return render_to_response(template, {
          'title': settings.TITLE_PREFIX,
          'specs_packages': specs_names,
          'version': version
        })
  else:
    return render_to_response(template, {
      'title': settings.TITLE_PREFIX,
      'specs': ','.join(presets),
      'version': version
    })

def _get_all_specs_packages(version):
  if not version:
    version = settings.DEFAULT_VERSION

  specs = []
  for name, project in settings.PROJECTS[version].iteritems():
    specs.extend(_get_specs(version, name))
  return specs

def _get_specs(version, name):
  project = _get_project(version, name)
  if project.has_key('specs'):
    return project['specs']
  else:
    return []

def _read_yaml(path):
  try:
    return yaml.load(file(path))
  except:
    LOG.exception("Could not parse: " + path)
    raise


def moorunner(request, path):
  """ Returns an asset from the MooTools Jasmine test runner. """
  return read_asset(os.path.normpath(settings.MOOTOOLS_RUNNER_PATH + '/' + path))


def format_code(extension, code_str):
  """Fix indent and highlight code"""
  try:
    lexer = get_lexer_by_name(extension, tabsize=2)
    return highlight(code_str, lexer, HtmlFormatter())
  except KeyError:
    LOG.warn('Cannot find lexer for extension %s' % (extension,))
    return "<div><pre>%s</pre></div>" % (code_str,)

# VIEW SOURCE
def view_source(request, version):
  """ Returns the contents of a given project/path combination in the view-source viewer. Reads
      yaml files that configure addtional sources to include in the view. """

  project_name = request.REQUEST.get('project')
  path = request.REQUEST.get('path')
  if project_name is None or path is None:
    raise Exception("You must specify a project and a path.")

  projects, dir_map = get_test_files(version)
  project = _get_project(version, project_name)
  full_path = os.path.normpath(get_path(project['demos']['path'])+path)

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
          file_data = get_depender(version).get((js_pkg, js_comp))
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
      'current': make_demo_url(version, project_name, path),
      'projects': projects,
      'title_prefix': settings.TITLE_PREFIX,
      'version': version
    }
  )


# DOCS
def viewdoc(request, version, path):
    parsed, path = _read_md(path)
    dirs, files = get_docs_files(version)

    def replacer(matchobj):
      match = matchobj.group(0)
      match = re.sub('\{#|}', '', match)
      return '<a class="toc_anchor" name="' + match + '"></a><a href="#top" class="to_top">back to top</a>'

    parsed = re.sub("\{#.*?}", replacer, parsed)

    return render_to_response('markdown.mako',
      {
        'body': parsed,
        'docs': files,
        'title': make_title(path.split('/')[-1]),
        'title_prefix': settings.TITLE_PREFIX,
        'current': 'viewdoc/' + path,
        'dirs': dirs,
        'toc': get_toc(parsed)
      }
    )

def _fix_md_extension(path):
  if not re.search("md$(?i)", path):
    path = path + '.md'
  return path

def _read_md(path):
  if path == '':
    path = "test-runner/WELCOME"
  path = _fix_md_extension(path)

  text = None
  if '..' in path:
    raise Exception('invalid path: %s' % path)
  else:
    md = os.path.abspath(os.path.join(settings.DOC_ROOT, '../../', path))
    if os.path.isfile(md):
      text = open(md, 'rb').read()
  if text is None:
    raise Exception("The path %s was not found." % path)
  else:
    return (markdown(text), path)

def get_toc(content):
  return re.findall("\{#(.*?)}", content)

def toc(request, path):
  toc = get_toc(_read_md(path)[0])
  basepath = request.REQUEST.get('basepath')
  return render_to_response('toc.mako',{
    'basepath': basepath,
    'toc': toc
  })

#  NAVIGATION
def top_nav(request, version):
  """ Renders the top navigation frame. """

  version_settings = get_version_settings(version)
  versions = []
  for name, v in settings.PROJECTS.iteritems():
    versions.append(name)

  return render_to_response('top_nav.mako', {
    'title': settings.TITLE_PREFIX,
    'settings': version_settings,
    'version': version,
    'versions': versions
  })

def bottom_frame(request, version):
  """ Given a url for the menu_path and content_path renders the bottom frames. """
  menu = request.REQUEST.get('menu_path')
  content = request.REQUEST.get('content_path')
  return render_to_response('bottom_frame.mako', {
    'title': settings.TITLE_PREFIX,
    'menu': menu,
    'content': content
  })

def demo_menu(request, version):
  """ Renders a menu with a list of all available tests. """
  projects, dir_map = get_test_files(version)
  return render_to_response('left_menu.mako',
    {
      'projects': projects,
      'title': 'Demos',
    }
  )

def docs_menu(request, version, project=None, path=None):
  """ Renders a menu with a list of all available docs. """
  projects, dir_map = get_docs_files(version)

  if version and project and path:
    path = _fix_md_extension(path)
    file_path = get_path(settings.PROJECTS[version][project]['docs']) + '/' + path
    toc = get_toc(_read_md(file_path)[0])
  else:
    path = None
    file_path = None
    toc = None

  return render_to_response('left_menu.mako',
    {
      'projects': projects,
      'title': 'Docs',
      'current_project': project,
      'current_path': path,
      'toc': toc
    }
  )



# ASSETS
def get_source_file(request, project=None, path=None):
  """ Given a project returns the contents of a file in its /Source directory. """
  if project == None:
    project = request.REQUEST.get('project')
  if project == None:
    raise Exception("The project %s is invalid." % project)

  if '..' in path:
    raise Exception("The path %s is invalid." % path)
  full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", project, "Source", path))
  return read_asset(full_path)

def asset(request, version=None, project_name=None, path=None):
  """ Given a project returns a file located in the test configuration path inside a subdirecotry called _assets. """

  if version is None:
    version = request.REQUEST.get('version', settings.DEFAULT_VERSION)
  if project_name == None:
    project_name = request.REQUEST.get('project')
  if project_name == None:
    raise Exception("The project %s is invalid." % project_name)

  project_dir = _get_project(version, project_name)['demos']['path']
  if '..' in path:
    raise Exception("The path %s is invalid." % path)
  full_path = os.path.normpath(project_dir + "/_assets/" + path)
  return read_asset(full_path)

def assets(request, project_name, path, version=None):
  """ Deprecated """
  return asset(request, version, project_name, path)

def generic_asset(request, path, version=None):
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

## DEPRECATED ECHOS

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
    " OLD: echo REQUEST['html'] "
    if delay:
        time.sleep(random.uniform(1,3))
    t = req.REQUEST.get('html','')
    return HttpResponse(t)

def ajax_xml_echo(req, delay=False):
    " OLD: echo REQUEST['xml'] "
    if delay:
        time.sleep(random.uniform(1,3))
    t = req.REQUEST.get('xml','')
    return HttpResponse(t, mimetype='application/xml')

def ajax_json_response(req):
    " OLD: standard JSON response "
    response_string = req.REQUEST.get('response_string','This is a sample string')
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
def get_files_by_project(version, project, directory, matcher, url_maker, dirs = None, file_map = None, include_root = None, flat_name = None, get_name_from_path = None):
  """ Given a project and a direcotry, returns all files in that directory that match the specified 'matcher' regular expression. """
  if dirs is None:
    dirs = {}
  if file_map is None:
    file_map = {}
  if get_name_from_path is None:
    def get_name_from_path(path):
      return path.split('/')[-1]

  def get_file_dict(files, directory):
    return dict([(url_maker(version, project, file.replace(directory, '')), make_title(get_name_from_path(file))) for file in files])

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
      if flat_name:
        if len(dirs[project_title]) == 0:
          dirs[project_title].append(dict(
            subdir = flat_name,
            title = make_title(flat_name),
            files = [],
            file_dict = {}
          ))
        d = dirs[project_title][0]
        d['files'].extend(matching_files)
        d['file_dict'] = dict(d['file_dict'].items() + get_file_dict(matching_files, directory).items())
      else:
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


def get_files(version, locations, matcher, url_maker, flat_name=None, get_name_from_path=None):
  """ Given a dict of locations, finds all files in those locations that match the specified 'matcher' regular expression.  """
  dirs = {}
  file_map = {}

  for project, directory in locations.iteritems():
    get_files_by_project(version, project, directory, matcher, url_maker, dirs, file_map, include_root = "/..", flat_name=flat_name, get_name_from_path=get_name_from_path)

  return dirs, file_map

def get_test_files(version, url_maker=None):
  """ Given a specified project, return all the HTML files in that configured path from the settings.
      If no project is specified, returns all HTML files in all the configured test directories."""
  if url_maker == None:
    url_maker = make_demo_url

  paths = {}
  for name, project in settings.PROJECTS[version].iteritems():
    if project.has_key('demos'):
      if not project['demos'].has_key('exclude') or project['demos']['exclude'] is False:
        paths[name] = get_path(project['demos']['path'])

  dirs, file_map = get_files(version, paths, matcher=HTML_MATCHER, url_maker=make_demo_url)

  paths = {}
  for name, project in settings.PROJECTS[version].iteritems():
    if project.has_key('fiddles'):
      if not project['fiddles'].has_key('exclude') or project['fiddles']['exclude'] is False:
        paths[name] = get_path(project['fiddles']['path'])
  def get_name_from_path(path):
    return path.split('/')[-2]
  dirs2, file_map2 = get_files(version, paths, matcher=HTML_MATCHER, url_maker=make_fiddle_url, flat_name='Fiddles', get_name_from_path=get_name_from_path)
  dirs = dict(dirs.items() + dirs2.items())
  file_map = dict(file_map.items() + file_map2.items())

  return dirs, file_map

def get_docs_files(version):
  """ Gets all markdown documents in a specified project or, if none is specified, all the markdown
      files in all the specified docs directories from the settings. """
  paths = {}
  for name, project in settings.PROJECTS[version].iteritems():
    if project.has_key('docs'):
      paths[name] = project['docs']
  return get_files(version, locations=paths, matcher=MARKDOWN_MATCHER, url_maker=docs_url)

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
def make_demo_url(version, project, path):
  """ Given a path and a project, returns a url for the demo."""
  return '/' + version + '/demo/?project='+quote(project)+'&path='+path

def make_title(path):
  """ Given a path, return a suiteable title for the file name."""
  return re.sub('[\._]', ' ', re.sub('(\.(html|mako|md|markdown))', '', path))

def docs_url(version, project, path):
  """ Given a project and a path, return the url for the docs. """
  root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
  project_path = get_path(_get_project(version, project)['docs'])
  docs_path = project_path.replace(root, '')
  return os.path.normpath('/' + version + '/viewdoc/' + docs_path + path);

def _force_unicode(data):
  """Encodings of the js files are unclear; force things
  into unicode, somewhat hackily."""
  try:
    data = unicode(data, "utf-8")
  except UnicodeDecodeError:
    data = unicode(data, "latin1")
  return data

def _get_project(version, name):
  version_settings = get_version_settings(version)
  if version_settings.has_key(name):
    return version_settings[name]
  if version_settings.has_key(name.lower()):
    return version_settings[name.lower()]
  if version_settings.has_key(name.capitalize()):
    return version_settings[name.capitalize()]

def make_fiddle_url(version, project, path):
  """ Given a path and a project, returns a url for the demo."""
  return '/' + version + '/' + project + '/fiddle' + path

def read_file(path):
  if not os.path.isfile(path):
    raise Exception("The file %s was not found." % path)
  return open(path, "rb").read()


def fiddle(request, project, version, demo_name):
  fiddle = _get_fiddle_details(project, version, demo_name)
  return render_to_response('fiddle.mako',
    {
      'title': make_title(demo_name),
      'demo_name': demo_name,
      'css': fiddle['css'],
      'html': fiddle['html'],
      'details': fiddle['details'],
      'package': fiddle['package_name'],
      'version': version,
      'project': project
    }
  )

def fiddle_source(request, version, project, demo_name):
  fiddle = _get_fiddle_details(project, version, demo_name)
  return render_to_response('view_fiddle_source.mako',
    {
      'js': format_code('js', fiddle['js']),
      'html': format_code('html', fiddle['html']),
      'css': format_code('css', fiddle['css']),
      'title': make_title(demo_name),
      'version': version,
      'demo_name': demo_name,
      'project': project
    }
  )

def fiddle_asset(request, version, project, demo_name, asset_path):
  fiddle = proj = _get_project(version, project)
  return read_asset(proj['fiddles']['path'] + '/' + asset_path)

def _get_fiddle_details(project, version, demo_name):
  proj = _get_project(version, project)
  base_path = proj['fiddles']['path']
  demo_dir = os.path.normpath(base_path)
  package = _read_yaml(proj['fiddles']['package'])
  raw_details = read_file(os.path.normpath(demo_dir + '/' + demo_name + '/demo.details'))
  return {
    'package_name': package['name'],
    'css': read_file(os.path.normpath(demo_dir + '/' + demo_name + '/demo.css')),
    'html': read_file(os.path.normpath(demo_dir + '/' + demo_name + '/demo.html')),
    'js': read_file(os.path.normpath(demo_dir + '/' + demo_name + '/demo.js')),
    'details': COMMENT_BLOCK.sub('', raw_details)
  }