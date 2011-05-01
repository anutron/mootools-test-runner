<%namespace name="components" file="demo_components.mako" />
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <title>${title_prefix} - ${title}</title>
    <link rel="stylesheet" href="/static/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
    <link rel="stylesheet" href="/static/css/docs.css" type="text/css" media="screen" title="no title" charset="utf-8">
  </head>
  <body>
    <div class="markdown">
     ${body}
    </div>
  </body>
</html>