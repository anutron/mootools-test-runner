import time
import simplejson
from django.http import HttpResponse, HttpResponseRedirect

def mootools_request_php(req):
  """ Recreates Request.php from the MooTools specs runner environment. """
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