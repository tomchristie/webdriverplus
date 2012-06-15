#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import re
import os
import sys

PACKAGE = 'webdriverplus'

base_dir = os.path.dirname(__file__)
module = os.path.join(base_dir, PACKAGE, '__init__.py')
version = eval(re.search('VERSION = (.*)', open(module).read()).group(1))
version_str = '%d.%d.%d' % (version[0], version[1], version[2])

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    print "You probably want to also tag the version now:"
    print "  git tag -a %s -m 'version %s'" % (version, version)
    print "  git push --tags"
    sys.exit()

f = open('requirements.txt', 'r')
lines = f.readlines()
requirements = [l.strip().strip('\n') for l in lines if l.strip() and not l.strip().startswith('#')]

setup(
    name=PACKAGE,
    version=version_str,
    url='http://webdriverplus.org',
    license='BSD',
    description='WebDriver Plus.',
    author='Tom Christie',
    packages=[PACKAGE],
    package_dir={PACKAGE: PACKAGE},
    include_package_data=True,
    test_suite='runtests.main',
    install_requires=requirements,
)
