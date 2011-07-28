<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <title>${title}</title>
    <link rel="stylesheet" href="/static/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
    <link rel="stylesheet" href="/static/css/shared.css" type="text/css" media="screen" title="no title" charset="utf-8">
    <link rel="stylesheet" href="/static/css/tests.css" type="text/css" media="screen" title="no title" charset="utf-8">
    <script src="/depender/build?require=${package}/${demo_name}"></script>
    <style>
      UL {
        list-style: none;
        margin: 0;
        padding: 0;
      }
      ${css|n}
    </style>
  </head>
  <body>
    ${details|n}
    <hr/>
    ${html|n}
    <div id="mt-test-buttons">
        <a class="btn-source minibutton" href="/${version}/${project}/fiddle_source/${demo_name}"><span><span class="icon"></span>view source</span></a>
    </div>
    
  </body>
</html>