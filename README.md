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

Writing test menus
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