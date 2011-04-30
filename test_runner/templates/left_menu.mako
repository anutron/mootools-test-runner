<%def name="print_toc(toc)">
  % for item in toc:
    <% 
      klass = ""
      if ":" not in item:
        klass = "toc_section"
    %>
    <li class="toc ${klass}"><a href="#${item}">${item}</a></li>
  % endfor
</%def>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <link rel="stylesheet" href="/static/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
    <link rel="stylesheet" href="/static/css/shared.css" type="text/css" media="screen" title="no title" charset="utf-8">
    <link rel="stylesheet" href="/static/css/left_menu.css" type="text/css" media="screen" title="no title" charset="utf-8">
    <link rel="stylesheet" href="/static/css/autocompleter.css" type="text/css" media="screen" title="no title" charset="utf-8">
    <script src="/static/js/mootools-core-1.3.2.js" type="text/javascript" charset="utf-8"></script>
    <script src="/static/js/mootools-more-1.3.2.js" type="text/javascript" charset="utf-8"></script>
    <script src="/static/js/autocompleter.js" type="text/javascript" charset="utf-8"></script>
    
    <script>
      window.addEvent('domready', function(){
        new OverText('filter');
        var terms = [];
        var term_map = {};
        $$('li a').each(function(a){
          terms.push(a.innerHTML);
          term_map[a.innerHTML] = a;
        });
        var filter = $('filter');
        var ac = new Autocompleter.Local(filter, terms, {
          width: 153,
          minLength: 1,
          selectMode: 'type-ahead',
          overflow: true,
          filterSubset: true
        });
        top.addEvent('keydown', function(e){
          filter.focus();
        });
        window.addEvent('keydown', function(e){
          filter.focus();
        });
        filter.addEvent('keydown', function(e){
          if (e.key == 'enter'){
            var value = this.get('value');
            if (term_map[value]) {
              top.frames['bottom_frame'].frames['content'].location.href = term_map[value].href;
            }
            ac.hideChoices();
            filter.value = '';
            filter.blur.delay(20, $('filter'));
          }
        });
      });
    </script>
  </head>
  <body>
    <div class="mt-nav">
      <h1>
        ${title}
        <div id="filter_wrapper"><input id="filter" title="Search"></div>
      </h1>
      % if projects is not None:
        % for project, directories in sorted(projects.items()):
          % if not excluded_tests or project not in excluded_tests:
            <h2>${project}</h2>
            % for directory in sorted(directories):
              <dl class="mt-tests">
                % if len(directory['title'].strip()) > 0 and directory['subdir'] != '.':
                  <dt>${directory['title']}</dt>
                % endif
                <dd>
                  <ul>
                    % for file_path, file_title in sorted(directory['file_dict'].items(), key=lambda x: x[1].lower()):
                      <li><span></span><a target="content" href="${file_path}">${file_title}</a></li>
                        % if toc and klass is not "":
                          ${print_toc(toc)}
                        % endif
                      % endfor
                  </ul>
                </dd>
              </dl>
            % endfor
          % endif
        % endfor
      % endif
    </div>
  </body>
</body>