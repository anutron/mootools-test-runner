<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ko">
<head>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
  <title>Specs for ${title}</title>

% if specs:


  <!-- Jasmine -->

  <link rel="stylesheet" type="text/css" href="/moorunner/Jasmine/jasmine.css">
  <link rel="stylesheet" type="text/css" href="/moorunner/runner.css">

  <script type="text/javascript" src="/moorunner/Jasmine/jasmine.js"></script>

  <!-- Specs -->
  <script type="text/javascript" src="/moorunner/Helpers/jasmine-html.js"></script>
  <script src="/static/js/query-string.js"></script>

  <script type="text/javascript" charset="utf-8" src="/moorunner/Helpers/Syn.js"></script>
  <script type="text/javascript" charset="utf-8" src="/moorunner/Helpers/JSSpecToJasmine.js"></script>

  <script src="/moorunner/Helpers/Sinon.JS/lib/sinon.js" type="text/javascript"></script>
  <script src="/moorunner/Helpers/Sinon.JS/lib/sinon/util/event.js" type="text/javascript"></script>
  <script src="/moorunner/Helpers/Sinon.JS/lib/sinon/util/fake_timers.js" type="text/javascript"></script>
  <script src="/moorunner/Helpers/Sinon.JS/lib/sinon/util/timers_ie.js" type="text/javascript"></script>
  <script src="/moorunner/Helpers/Sinon.JS/lib/sinon/util/fake_xml_http_request.js" type="text/javascript"></script>
  <script src="/moorunner/Helpers/Sinon.JS/lib/sinon/util/xhr_ie.js" type="text/javascript"></script>

  <script type="text/javascript" charset="utf-8">

  (function(){

  // Load all the specs

  window.onload = function(){
    // Run the specs
    jasmine.getEnv().addReporter(new jasmine.TrivialReporter());
    jasmine.getEnv().execute();
  };

  })();
  </script>
  </head>
  <body>
    <script type="text/javascript" src="/depender/build?requireLibs=${specs}&version=${version}"></script>
% else:
    <link rel="stylesheet" href="/static/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
    <link rel="stylesheet" type="text/css" href="/static/css/specs.css"/>
    <script src="/static/js/multi-select-checkboxes.js"></script>
    <script src="/static/js/mootools-core-1.3.2.js" type="text/javascript" charset="utf-8"></script>
    <script>
      window.addEvent('domready', function(){
        $('clear').addEvent('click', function(e){
          e.stop();
          $$('input[type=checkbox]').set('checked', '');
        });
        $('all').addEvent('click', function(e){
          e.stop();
          $$('input[type=checkbox]').set('checked', 'true');
        });
      });
    </script>
  </head>
  <body>
    <div class="mt-specs">
      <p>Choose the specs you wish to run:</p>
      <form method="get">
        <ul>
          % for package in specs_packages:
            <li><input name="preset" value="${package}" type="checkbox" checked="checked">${package}</li>
          % endfor
        </ul>
        <input type="submit" value="Run selected"/>
        <hr/>
        <div class="mt-specs-actions">
          <button id="clear">Clear selection</button>
          <button id="all">Select all</button>
          <p style="font-size:smaller; padding-left: 8px">Hold shift and click to select ranges.</p>
        </div>
      </form>
    </div>
% endif
  </body>
</html>
