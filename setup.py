#!/usr/bin/env python
"""This project provides the expanded versions of standard Python datetime/timedelta classes,
capable for more operations (e.g. divide timedelta by timedelta).
"""
try:
    from setuptools import setup
except:
    from distutils.core import setup


from contrib.distutils_googlecode_upload.googlecode_distutils_upload import upload as googlecode_upload
from contrib.wikir.commands import publish_wiki

# Classifiers as in http://pypi.python.org/pypi?:action=list_classifiers
CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.0
Programming Language :: Python :: 3.1
Programming Language :: Python :: 3.2
Topic :: Software Development
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Utilities
"""

setup(
    name = "datetimeex",
    version = "0.1",
    description = __doc__.split("\n", 1)[0],
    long_description = __doc__.split("\n", 2)[-1],
    author = "Alexander Myodov",
    author_email = "amyodov@gmail.com",
    url = "http://code.google.com/p/python-datetimeex/",
    packages = ["datetimeex",],
    classifiers = [c for c in CLASSIFIERS.split("\n") if c],
    license = "New BSD License",
    platforms = ["any"],
    cmdclass = {"googlecode_upload" : googlecode_upload,
                "publish_wiki"      : publish_wiki,}
)
