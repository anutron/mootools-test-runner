<%!
  from django.core.urlresolvers import reverse
%>
<%def name="header(title='MooTools Test Framework', projects=False, current=None, previous=None, next=None, excluded_tests=None)">
  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
  <html>
    <head>
      <title>${title_prefix} - ${title}</title>
      <link rel="stylesheet" href="/static/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
      <link rel="stylesheet" href="/static/css/shared.css" type="text/css" media="screen" title="no title" charset="utf-8">
      <link rel="stylesheet" href="/static/css/tests.css" type="text/css" media="screen" title="no title" charset="utf-8">
      <script src="/static/js/test-helpers.js"></script>
    </head>
      <div id="mt-loading">Loading...</div>
</%def>

<%def name="footer()">
      <script>
        document.body.className = 'loaded';
      </script>
    </body>
  </html>
</%def>

<%def name="nav(current=None, view='test')">
  <div id="mt-test-buttons">
    % if view == 'test' and test:
      <a class="btn-source minibutton" href="/source/${current}"><span><span class="icon"></span>view source</span></a>
    % elif view == 'source':
      <a class="btn-left minibutton" href="${current}"><span><span class="icon"></span>back to test</span></a>
    % endif
  </div>
</%def>
