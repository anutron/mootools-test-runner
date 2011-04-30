<%!
  from django.core.urlresolvers import reverse
%>
<%def name="header(title='MooTools Test Framework', projects=False, current=None, previous=None, next=None, excluded_tests=None)">
  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
  <html>
    <head>
      <title>${title_prefix} - ${title}</title>
      <link rel="stylesheet" href="/static/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
      <link rel="stylesheet" href="/static/css/tests.css" type="text/css" media="screen" title="no title" charset="utf-8">
      <script src="/static/js/test-helpers.js"></script>
    </head>
      <div id="mt-content">
        <div id="mt-loading">Loading...</div>
</%def>

<%def name="footer()">
      </div>
      <script>
        document.body.className = 'loaded';
      </script>
    </body>
  </html>
</%def>

<%def name="nav(title, projects=None, current=None, previous=None, next=None, view='test', excluded_tests=None)">
  <div id="mt-content_header">
    <h2>${title}</h2>
    <div>
    % if previous:
      <a class="mt-prev minibutton btn-left" href="${previous}"><span><span class="icon"></span>previous (${prev_name})</span></a>
    % endif
    % if next:
    <a class="mt-next minibutton btn-right" href="${next}"><span><span class="icon"></span>next (${next_name})</span></a>
    % endif
    % if view == 'test' and test:
      <a class="btn-source minibutton" href="/source/${current}"><span><span class="icon"></span>view source</span></a>
    % elif view == 'source':
      <a class="btn-left minibutton" href="${current}"><span><span class="icon"></span>back to test</span></a>
    % endif
    </div>
  </div>
  <div id="mt-log-wrapper"><div id="mt-log"></div></div>
</%def>
