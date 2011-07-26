<%namespace name="components" file="demo_components.mako" />

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
	<head>
		<title>${title_prefix} - ${title}</title>
		<link rel="stylesheet" href="/static/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
		<link rel="stylesheet" href="/static/css/tests.css" type="text/css" media="screen" title="no title" charset="utf-8">
		<link rel="stylesheet" href="/static/css/minibuttons.css" type="text/css" media="screen" title="no title" charset="utf-8">
	</head>
	<body>
		<div class="view_source">
			${components.nav(current=current, view="source", version=version)}
			<div class="source">
				<h3>Relevant sources</h3>
				<a name="top"></a>
				<ul>
					<li class="tab html-tab"><a href="#html">HTML Test</a></li>
					%for js_name in js_data.iterkeys():
						<li class="tab">
							<a href="#${js_name}">${js_name}</a>
						</li>
					%endfor
				</ul>
				<h3>Source for HTML</h3>
				<a href="html"></a>
				${data|n}

				## JS data
				%for js_name, js in js_data.iteritems():
					<a name="${js_name}"></a>
					<h3>Source for <code>${js_name}</code>
						<a class="totop" href="#top">back to top</a>
					</h3>
					${js|n}
				%endfor

			</div>
		</div>
	</body>
</html>
