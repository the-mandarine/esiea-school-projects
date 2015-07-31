"""PyMAS setup script"""

from distutils.core import setup, find_packages
setup(
    name = 'PyMAS',
    version = '0.1dev',
    author = "PyMAS Team",
    author_email = "pymas@us-robotics.net",
    packages = ['pymas'],
    url = "http://pypi.python.org/pypi/PyMAS",
    license = "LICENSE.txt",
    description = 'Python Multi-Agent System scheduler',
    long_description = open('README.rst').read(),
    install_requires = [],
)


