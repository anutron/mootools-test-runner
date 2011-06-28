<%def name="print_toc(toc, file_path = '')">
  <ul class="toc">
    % for item in toc:
      % if ':' in item:
        <li class="toc toc_section"><a target="content" href="${file_path}#${item}">${item.split(':')[1]}</a></li>
      % endif
    % endfor
  </ul>
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
        var AC = new Class({
          Extends: Autocompleter.Local,
          showChoices: function(){
            this.parent.apply(this, arguments);
            this.choices.position({
                relativeTo: this.element,
                position: 'bottomCenter',
                edge: 'topCenter',
                offset: { x: -4 }
            });
          }
        })
        var ac = new AC(filter, terms, {
          width: 166,
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
            select(term_map[value])
          }
        });
        filter.addEvent('blur', function(){
          filter.value = '';
        });
        
        var scrollTo = function(li){
          scroller.start(0, document.id(li).getPosition(document.body).y - 40);
        };
        
        var select = function(link){
          $$('.mt-selected').removeClass('mt-selected');
          var li = link.getParent('li').addClass('mt-selected');
          % if title == "Docs":
            var toc = $$('.toc')[0];
            if (toc) {
              toc.dissolve().get('reveal').chain(function(){
                toc.destroy();
                scrollTo(li);
              });
            }
            getTOC(link);
          % else:
            scrollTo(li);
          % endif
        };
        
        var scroller = new Fx.Scroll(document.body);
        
        $$('.mt-nav')[0].addEvent('click:relay(a.navlink)', function(e, link){
          select(link);
        });
        
        var getTOC = function(link){
          var li = link.getParent('li');
          new Request.HTML({
            spinnerTarget: li,
            useSpinner: true,
            spinnerOptions: {
              containerPosition: {
                position: 'upperRight',
                edge: 'centerRight',
                offset: {
                  y: 4
                }
              }
            },
            url:'/toc' + link.get('href').replace('viewdoc/', ''),
            onComplete: function(responseTree, responseElements, responseHTML, responseJavaScript){
              var toc = Elements.from(responseHTML)[0];
              toc.hide().inject(link, 'after').reveal();
            },
            data: {basepath: link.get('href')}
          }).send();
        };
        var first = $$('a.navlink')[0].addClass('mt-selected');
        % if title == "Docs":
          var currentTOC = $$('.toc')[0];
          if (!currentTOC) getTOC(first);
        % endif
      });
    </script>
  </head>
  <body>
    <h1>${title}</h1>
    <div class="mt-nav">
      <div id="filter_wrapper"><input id="filter" title="Search"></div>
      % if projects is not None:
        % for project, directories in sorted(projects.items()):
          <h2>${project}</h2>
          % for directory in sorted(directories):
            <dl class="mt-tests">
              % if len(directory['title'].strip()) > 0 and directory['subdir'] != '.':
                <dt>${directory['title']}</dt>
              % endif
              <dd>
                <ul>
                  % for file_path, file_title in sorted(directory['file_dict'].items(), key=lambda x: x[1].lower()):
                    <%
                      klass = ''
                      if current_project == project and current_path == file_path.split('/')[-1]:
                        klass = 'mt-selected'
                    %>
                    <li class="${klass}">
                      <span></span><a target="content" class="navlink" href="${file_path}">${file_title}</a>
                      % if klass != '' and toc:
                        ${print_toc(toc, file_path)}
                      % endif
                    </li>
                  % endfor
                </ul>
              </dd>
            </dl>
          % endfor
        % endfor
      % endif
    </div>
  </body>
</body>