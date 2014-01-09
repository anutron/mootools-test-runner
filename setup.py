from setuptools import setup, find_packages
import os

base = os.path.join(os.path.dirname(__file__), "frontend_dev")

setup(
      name = "mootools_frontend_dev",
      version = "0.1",
      url = 'http://www.mootools.net',
      description = "MooTools Test Suite",
      install_requires = ['setuptools', 'Django==1.4.1', 'PyYAML', 'simplejson', 'django_extensions', 'django-mako', 'werkzeug', 'Markdown', 'Pygments'],
      packages = find_packages(base),
      package_dir={'': base}
)
