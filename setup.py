# Copyright 2016 Kumoru.io
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from codecs import open
from distutils.core import Command
from setuptools import find_packages
from setuptools import setup

PARAMS = {}

PARAMS['name'] = 'logformatjson'
PARAMS['version'] = '0.1.0'
PARAMS['description'] = 'Json formatter for logging'

with open('README.rst', 'r', encoding = 'utf-8') as fh:
    PARAMS['long_description'] = fh.read()

PARAMS['url'] = 'https://github.com/kumoru/logformatjson'
PARAMS['author'] = 'Ryan Richard'
PARAMS['author_email'] = 'ryan@kumoru.io'
PARAMS['license'] = 'Apache 2.0'

PARAMS['classifiers'] = [
    'Development Status :: 4 - Beta',
    # 'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development :: Libraries',
    'Topic :: System :: Logging'
]

PARAMS['keywords'] = [
    'formatter',
    'json',
    'logging',
]

PARAMS['packages'] = find_packages()

PARAMS['tests_require'] = [
    'pylint',
    'pytest',
    'pytest-cov',
    'pytest-mock',
]

setup(**PARAMS)

