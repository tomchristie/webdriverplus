#!/usr/bin/env/python
# -*- coding: utf-8 -*-

from setuptools import setup

import re
import os

PACKAGE = 'webdriverplus'

base_dir = os.path.dirname(__file__)
module = os.path.join(base_dir, PACKAGE, '__init__.py')
version = eval(re.search('VERSION = (.*)', open(module).read()).group(1))
version_str = '%d.%d.%d' % (version[0], version[1], version[2])

setup(
    name=PACKAGE,
    version=version_str,
    url='http://webdriverplus.org',
    license='BSD',
    description='WebDriver Plus.',
    author='Tom Christie',
    packages=[PACKAGE],
    package_dir={PACKAGE: PACKAGE},
    test_suite='runtests.main',
)
