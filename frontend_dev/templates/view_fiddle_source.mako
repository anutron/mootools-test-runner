<%namespace name="components" file="demo_components.mako" />

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
	<head>
		<title>${title}</title>
		<link rel="stylesheet" href="/static/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
		<link rel="stylesheet" href="/static/css/tests.css" type="text/css" media="screen" title="no title" charset="utf-8">
		<link rel="stylesheet" href="/static/css/minibuttons.css" type="text/css" media="screen" title="no title" charset="utf-8">
	</head>
	<body>
		<div class="view_source">
		<div id="mt-test-buttons">
			<a class="btn-source minibutton" href="/${version}/${project}/fiddle/${demo_name}/demo.html"><span><span class="icon"></span>view fiddle</span></a>
		</div>
			
			<div class="source">
				<h3>Relevant sources</h3>
				<a name="top"></a>
				<ul>
					<li class="tab html-tab"><a href="#html">HTML</a></li>
					<li class="tab html-tab"><a href="#css">CSS</a></li>
					<li class="tab html-tab"><a href="#js">JS</a></li>
				</ul>

				<h3>Source for HTML</h3>
				<a name="html"></a>
				${html|n}

				<h3>Source for CSS</h3>
				<a name="css"></a>
				${css|n}


				<h3>Source for JS</h3>
				<a name="js"></a>
				${js|n}


			</div>
		</div>
	</body>
</html>
