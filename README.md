MooTools Test Runner
--------------------

quick setup:

	$ git clone http://github.com/anutron/mootools-test-runner.git
	$ git submodule update --init
	$ virtualenv env
	$ env/bin/python ext/depender/django/depender/setup.py develop
	$ env/bin/python setup.py develop
	$ env/bin/python manage.py runserver_plus

Then open http://localhost:8000/