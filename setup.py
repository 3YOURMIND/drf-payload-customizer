# Copyright 2018 3YOURMIND GmbH

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import path
from setuptools import setup


PROJECT_DIR = path.abspath(path.dirname(__file__))

long_description = open(path.join(PROJECT_DIR, 'README.md')).read()

setup(
    name='drf-payload-customizer',
    version='0.1.1',
    packages=['drf_payload_customizer','drf_payload_customizer.mixins'],
    url='https://github.com/3YOURMIND/drf-payload-customizer',
    license='Apache License 2.0',
    author='3YOURMIND',
    author_email='01tonythomas@gmail.com',
    description='This package allows you to customize your '
                'django-rest-framework serializer i/o to make modern frontend frameworks happy.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='django drf rest converter mapping case transformation'
)
