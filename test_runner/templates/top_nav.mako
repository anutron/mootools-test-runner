<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <link rel="stylesheet" href="/static/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
    <link rel="stylesheet" href="/static/css/shared.css" type="text/css" media="screen" title="no title" charset="utf-8">
    <link rel="stylesheet" href="/static/css/top_nav.css" type="text/css" media="screen" title="no title" charset="utf-8">
    <script src="/static/js/mootools-core-1.3.2.js" type="text/javascript" charset="utf-8"></script>
    <script>
    window.addEvent('domready', function(){
      //temporary; won't hold up when/if we add cross-linking between sections
      var links = $$('a');
      links.addEvent('click', function(e){
        links.removeClass('selected');
        var target = e.target;
        if (links.indexOf(target) == -1) target = target.getParent('a');
        target.addClass('selected');
      });
    });
    </script>
  </head>
  <body>
    <div id="mt-top-nav">
      <h1>${title}</h1>
      <ul>
        % if show_docs:
          <li><a target="bottom_frame" class="mt-docs minibutton selected"
            href="/bottom_frame?menu_path=/docs_menu&content_path=/welcome"><span>Docs</span></a></li>
        % endif
        % if show_demos:
          <li><a target="bottom_frame" class="mt-demos minibutton" 
            href="/bottom_frame?menu_path=/test_menu&content_path=/welcome"><span>Demos</span></a></li>
        % endif
        % if show_specs:
          <li><a target="bottom_frame" class="mt-specs minibutton" 
            href="/specs"><span>Specs</span></a></li>
        % endif
        % if show_benchmarks:
          <li><a target="bottom_frame" class="mt-benchmarks minibutton" 
            href="#"><span>Benchmarks</span></a></li>
        % endif
    </div>
  </body>
</body>