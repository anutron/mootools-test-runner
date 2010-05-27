from setuptools import setup, find_packages
import os

base = os.path.join(os.path.dirname(__file__), "src")

setup(
      name = "mootools_tests",
      version = "0.1",
      url = 'http://www.mootools.net',
      description = "MooTools Test Suite",
      install_requires = ['setuptools', 'django', 'PyYAML', 'simplejson'],
      packages = find_packages(base),
      package_dir={'': base}
)