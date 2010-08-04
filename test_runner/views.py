# Create your views here.

from djangomako.shortcuts import render_to_response, render_to_string
import os, re, time
from django.conf import settings
from django.http import HttpResponse
from markdown import markdown
from urllib import quote

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
      'previous': None
    }
  )

def asset(request, project, path):
  project_dir = settings.MOOTOOLS_TEST_LOCATIONS[project]
  full_path = os.path.normpath(project_dir + "/_assets/" + path)
  if not os.path.isfile(full_path):
    raise Exception("The path %s was not found." % path)


  image_data = open(full_path, "rb").read()
  if re.search("png$(?i)", path):
    return HttpResponse(image_data, mimetype="image/png")
  if re.search("jpg$(?i)", path):
    return HttpResponse(image_data, mimetype="image/jpg")
  if re.search("gif$(?i)", path):
    return HttpResponse(image_data, mimetype="image/gif")
  if re.search("css$(?i)", path):
    return HttpResponse(image_data, mimetype="text/css")
  if re.search("js$(?i)", path):
    return HttpResponse(image_data, mimetype="application/x-javascript")
  if re.search("flv$(?i)", path):
    return HttpResponse(image_data, mimetype="video/x-flv")
  if re.search("swf$(?i)", path):
    return HttpResponse(image_data, mimetype="application/x-shockwave-flash")
  
  raise Exception("Unknown asset type (currently only png/gif/jpg/css/js are supported).")

# the following ajax responses borrowed from MooShell - thx Piotr!
def ajax_json_echo(req, delay=True):
  " echo GET and POST "
  if delay:
    time.sleep(2)
  c = {'get_response':{},'post_response':{}}
  for key, value in req.GET.items():
    c['get_response'].update({key: value})
  for key, value in req.POST.items():
    c['post_response'].update({key: value})
  return HttpResponse(simplejson.dumps(c),mimetype='application/javascript')


def ajax_html_echo(req, delay=True):
  if delay:
    time.sleep(2)
  t = req.REQUEST.get('html','')
  return HttpResponse(t)


def ajax_xml_echo(req, delay=True):
  if delay:
    time.sleep(2)
  t = req.REQUEST.get('xml','')
  return HttpResponse(t, mimetype='application/xml')


def ajax_json_response(req):
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

def test(request):
  projects, dir_map = get_files()
  project = request.REQUEST.get('project')
  path = request.REQUEST.get('path')
  
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
    prev_name = make_title(prev)
  else:
    prev_name = None
  if next:
    next_name = make_title(next)
  else:
    next_name = None


  f = open(full_path)
  return render_to_response('test.mako', 
    {
      'test': f.read(),
      'title': make_title(path),
      'current': make_url(path, project),
      'projects': projects,
      'title_prefix': settings.TITLE_PREFIX,
      'previous': prev,
      'prev_name':prev_name,
      'next': next,
      'next_name':next_name,
    }
  )

HTML_MATCHER = re.compile("\.html$")

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

def get_file_dict(files, directory, project):
  return dict([(make_url(file.replace(directory, ''), project), make_title(file.split('/')[-1])) for file in files])

def make_url(path, project):
  return '?project='+quote(project)+'&path='+path

def make_title(path):
  return path.split('/')[-1].replace('.html', '').replace('_', ' ')
