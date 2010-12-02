<%!
	from django.core.urlresolvers import reverse
%>
<%def name="header(title='MooTools Test Framework', projects=False, current=None, previous=None, next=None)">
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
	<html>
		<head>
			<title>${title_prefix} - ${title}</title>
			<link rel="stylesheet" href="/static/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
			<link rel="stylesheet" href="/static/css/tests.css" type="text/css" media="screen" title="no title" charset="utf-8">
			<script>
			var makeActions = function(tests){
				try {
					if (!$('actions')) new Element('dt', {'id': 'actions'}).inject($('mt-content'), 'top');
					tests.each(function(test, i) {
						new Element('dt').adopt(
							new Element('a', {
								text: test.title,
								events: {
									click: test.fn
								},
								id: 'test-' + i
							})
						).inject('actions');
						if (test.description) new Element('dd', { text: test.description }).inject('actions');
					});
				} catch(e) {
					alert('Could not create actions. Check console for details.');
					console.log('Ensure you have Core/Element.Event - plus its dependencies.', e);
				}
			};
			var log = function(msg) {
				var type = function(obj){
					if (obj == undefined) return false;
					if (obj.nodeName){
						switch (obj.nodeType){
							case 1: return 'element';
							case 3: return (/\S/).test(obj.nodeValue) ? 'textnode' : 'whitespace';
						}
					} else if (typeof obj.length == 'number'){
						if (obj.callee) return 'arguments';
					}
					return typeof obj;
				};
				var parse = function(){
					var str = '';
					for (var i = 0; i < arguments.length; i++) {
						var value = arguments[i];
						switch (type(value)) {
							case 'element':
								str += value.tagName.toLowerCase();
								if (value.id) str += '#' + value.id;
								if (value.className) str += value.className.split(' ').join('.');
								break;

							case 'array':
								str +='[';
								var results = [];
								for (var index = 0; index < value.length; index++) {
									results.push(parse(value[index]));
								}
								str += results.join(', ') + ']';
								break;

							case 'object':
								var objs = [];
								for (name in value) {
									if (type(value[name]) != 'object') {
										objs.push(name + ': ' + parse(value[name]));
									} else {
										objs.push(name + ': (object)');
									}
								}
								str += '{' + objs.join(', ') + '}';
								break;

							case 'function':
								str += '(function)';
								break;

							case 'boolean':
								str += String(value);
								break;

							default: str += value;
						}
						if (i != (arguments.length - 1)) str += ' ';
					}
					return str;
				};
				document.getElementById('mt-log').innerHTML += parse.apply(this, arguments) + '<br/>';
			};
			</script>
		</head>
		<body class="not_loaded">
		
			${nav(title=title, projects=projects, current=current, previous=previous, next=next)}
			<div id="mt-content">
				<div id="mt-loading">Loading scripts...</div>
</%def>

<%def name="footer()">
			</div>
			<script>
				document.body.className = 'loaded';
			</script>
		</body>
	</html>
</%def>

<%def name="nav(title, projects=None, current=None, previous=None, next=None, view='test')">
	<div id="mt-nav">
		<h1><a href="/">${title_prefix}</a></h1>
		% if projects is not None:
			% for project, directories in sorted(projects.items()):
				<h2>${project}</h2>
				% for directory in sorted(directories):
					<dl class="mt-tests">
						<dt>${directory['subdir']}</dt>
						<dd>
							<ul>
								% for file_path, file_title in sorted(directory['file_dict'].items(), key=lambda x: x[1].lower()):
									<%
										klass = ""
										if file_path == str(current):
											klass = "mt-selected"
									%>
									<li class="${klass}"><span></span><a href="/test/${file_path}">${file_title}</a></li>
									% endfor
							</ul>
						</dd>
					</dl>
				% endfor
			% endfor
		% endif
	</div>
	<div id="mt-content_header">
		<h2>${title}</h2>
		<div>
		% if previous:
			<a class="mt-prev minibutton btn-left" href="/test${previous}"><span><span class="icon"></span>previous (${prev_name})</span></a>
		% endif
		% if next:
		<a class="mt-next minibutton btn-right" href="/test${next}"><span><span class="icon"></span>next (${next_name})</span></a>
		% endif
		% if view == 'test' and test:
		  <a class="btn-source minibutton" href="/source/${current}"><span><span class="icon"></span>view source</span></a>
		% elif view == 'source':
		  <a class="btn-left minibutton" href="/test/${current}"><span><span class="icon"></span>back to test</span></a>
		% endif
		</div>
	</div>
	<div id="mt-log-wrapper"><div id="mt-log"></div></div>
</%def>