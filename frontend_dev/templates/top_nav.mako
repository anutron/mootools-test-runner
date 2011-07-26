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
      $$('select')[0].addEvent('change', function(){
        window.parent.location.href = this.getSelected()[0].get('href');
      });
    });
    </script>
  </head>
  <body>
    <div id="mt-top-nav">
      <div class="title">
        <h1>${title}</h1>
        <span class="version">
          version: 
          <select>
            % for v in versions:
              <option
                href="/?version=${v}"
                % if v == version:
                  selected="true"
                % endif
              >${v}</option>
            % endfor
          </select>
        </span>
      </div>
      <ul>
        <li><a target="bottom_frame" class="mt-docs minibutton selected"
          href="/${version}/bottom_frame?menu_path=/${version}/docs_menu&content_path=/welcome"><span>Docs</span></a></li>
        <li><a target="bottom_frame" class="mt-demos minibutton" 
          href="/${version}/bottom_frame?menu_path=/${version}/demo_menu&content_path=/welcome"><span>Demos</span></a></li>
        <li><a target="bottom_frame" class="mt-specs minibutton" 
          href="/${version}/specs"><span>Specs</span></a></li>
        <li><a target="bottom_frame" class="mt-benchmarks minibutton" 
          href="/${version}/benchmarks/?preset=all"><span>Benchmarks</span></a></li>
        <li><a target="bottom_frame" class="mt-builder minibutton" 
          href="/depender/"><span>Builder</span></a></li>
      </ul>
    </div>
  </body>
</body>