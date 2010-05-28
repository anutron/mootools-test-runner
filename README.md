MooTools Test Runner
--------------------

quick setup:

	$ git clone http://github.com/anutron/mootools-test-runner.git
	$ git submodule update --init
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