MooTools Test Runner
--------------------

quick setup:

	$ git clone http://github.com/anutron/mootools-test-runner.git
	$ git submodule update --init
	$ cp settings_example.py settings.py
	$ virtualenv env
	$ env/bin/python ext/depender/django/setup.py develop
	$ env/bin/python setup.py develop
	$ env/bin/python manage.py runserver_plus

Then open http://localhost:8000/

requirements:

* [virtualenv](http://pypi.python.org/pypi/virtualenv)
* [python](http://www.python.org/)

To install virtualenv on OSX, [follow these instructions](http://www.fprimex.com/coding/pymac.html):

	# Install easy_install and virtualenv into the system wide python package dir
	curl -O http://peak.telecommunity.com/dist/ez_setup.py > ez_setup.py
	sudo python ez_setup.py
	sudo easy_install virtualenv
	rm ez_setup.py

Validating the Dependency map
==================

When you request JavaScript for a test (see section below on Writing Tests) the [Depender](http://github.com/anutron/mootools-depender) application (included via submodule) maps the dependencies for your requested components and loads all the related JavaScript. If your dependency map is incomplete or contains errors your test will fail to load (see section below on this topic).

You can validate your entire dependency map from the command line. This is recommended if you are using libraries that are not included via the default submodules (which have been verified to have valid dependency maps):

	$ env/bin/python ext/depender/django/mootools/manage.py depender_check

This should print out the entire dependency map for you. If it throws errors, you must resolve the conflicts before you can include the errant source files.

When Tests Fail To Load
=================

Sometimes a test will have a problem. When this happens, your browser will do one of the following:

* If the test fails because the dependency map is invalid *and* _the test suite is not in debug mode_, you will see an alert that something has gone wrong in the attemp to load the JavaScript for that test. If you are running the server yourself, check the output from the command line to see the error.
* If the test fails because the dependency map is invalid but the test suite is in debug mode, nothing will happen. This is because the `script` file that included the JavaScript for the test (See section below on authoring tests) has thrown an error and the server has returned a debugging console (HTML) instead of a JavaScript response. You can open the source of that JavaScript tag and view this console which can be helpful in debugging the issue.
* If the test fails because of a problem in your JavaScript itself (syntax errors and the like) you'll want to use a debugger like [Firebug](http://getfirebug.com) to determine the issue.

Debug Settings
==============

In `settings.py` there are two debug settings. One is at the top and in the settings example is set to `Debug = True`. When this value is set the server displays an HTML response with a debug console in your browser when things fail. This includes requests for scripts that have missing dependencies. As a result, nothing happens in the browser because the `script` tag gets back an HTML response and just dies. Open the source url for the script tag to see the stack trace. Set `Debug = False` and you'll get an alert that there has been an error, though this alert is not very informative (but at least you are made aware of it).

The other debug statement is `DEPENDER_DEBUG = True` (this is default). This setting forces the Depender app to reload the JavaScript from the disk every time you request anything, which is rather slow, but useful for development. Set this to `False` to force it to cache everything in memory, which is much faster.

Writing Tests
=============

Tests are simple html files that contain inline css or style tags, HTML tags, and script tags. Typically they do not use any sort of domready function but rather rely upon load order for referencing the DOM. Here's a simple test that sets the style of an element:

	<p>I set the style of the box below from red to blue and back when the link below is clicked.</a>
	<div id="box" style="height: 100px; width: 100px; background: red;"></div>
	<a id="toggle">Toggle the color</a>
	<script src="/depender/build?require=Core/Element.Event,Core/Element.Style"></script>
	<script>
		var currentColor = 'red';
		$('toggle').addEvent('click', function(){
			if (currentColor == 'red') currentColor = 'blue;
			else currentColor = 'red';
			$('box').setStyle('background', currentColor);
		});
	</script>

As seen in the above example, there is some HTML that explains what the test does (it is highly recommended that you include it). Then some HTML for the test itself. Finally, a script tag that requires the needed components from [Depender](http://github.com/anutron/mootools-depender) and a script that sets up and runs your test.

This content is put in an HTML file in one of your included libraries' /Tests directory.

Writing Test Menus
==================

To aid in authoring a log of functions to run in a context there's a helper function included in the test runner. If you have a test that has numerous states you want to test (for example, an effect you want to run several times with different arguments) you can easily generate a menu for users. Simply call `makeActions` and pass it an array of objects with test information like this:

	var fx = new Fx.Scroll('scrollExample', {duration: 500});
	makeActions([
		{
			title: 'Scroll the box to the bottom.',
			description: 'If you define a description, this shows up below the button; this is optional!',
			fn: fx.toBottom.bind(fx)
		},
		{
			title: 'Scroll the box to the right.',
			fn: function(){
				fx.toRight();
			}
		}
	]);

Note that to use this method you have to include `Element.Event` in your test before you call makeActions, like so:

	<script src="/depender/build?require=Core/Element.Event"></script>

Also note that the menu is injected into a definition list with the id `actions`. If it can't find one, it will inject one for you. If you want to control where this menu shows up in the DOM of your test, include an empty definition list:

	<dl id="actions"></dl>

Assets
======

If you need to include an external asset with your test (an image, css file, etc) you must reference it with the following path formula:

	/asset/[project name]/[file name]

In addition to this, the file in question must exist in a directory called `_assets` in your test directory.

Ajax Helpers
============

The test framework comes with several Ajax helpers for your tests. These are:

### /echo/js

Returns whatever you send as POST or GET value "js" as application/javascript mime type.
Pass in value for "delay" for any delay you want (eg. delay=5 for 5 seconds).

### /echo/json

Returns whatever you send as POST or GET value "json" as application/javascript mime type. If an error is thrown it is returned as json. If no value is sent "{}" is returned.
Pass in value for "delay" for any delay you want (eg. delay=5 for 5 seconds).

### /echo/jsonp

Returns any POST or GET params encoded as json values wrapped in whatever you specify as "callback"
Pass in value for "delay" for any delay you want (eg. delay=5 for 5 seconds).

### /echo/html

Returns whatever you send as POST or GET value "html".
Pass in value for "delay" for any delay you want (eg. delay=5 for 5 seconds).

Old Ajax Helpers
================

### /ajax_json_response

Returns a JSON encoded response containing a `string`, `object`, and `array`. Specify a value for `response_string` in the POST or GET parameters to set the string explicitly. This response is returned with the `application/javascript` mimetype. Specify a `callback` option if you want to wrap the JSON in a function call.

### /ajax_html_javascript_response

Returns a standard HTML response that contains a paragraph and a `script` tag with an alert in it.

### /ajax_json_echo

Returns a JSON response of all the GET and POST parameters of your request with an `application/javascript` mimetype. Specify a `callback` option if you want to wrap the JSON in a function call.


### /ajax_html_echo

Returns a response containing whatever you specify in the `html` GET or POST value.

### /ajax_xml_echo

Returns a response containing whatever you specify in the `xml` GET or POST value with a `application/xml` mime type.

