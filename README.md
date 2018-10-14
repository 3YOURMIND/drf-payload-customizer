
[![License](https://img.shields.io/github/license/3yourmind/drf-payload-customizer.svg)](./LICENSE)
[![Contributing](https://img.shields.io/badge/PR-welcome-green.svg)](https://github.com/3YOURMIND/drf-payload-customizer/pulls)
[![3yourminD-Careers](https://img.shields.io/badge/3YOURMIND-Hiring-brightgreen.svg)](https://www.3yourmind.com/career)
[![Stars](https://img.shields.io/github/stars/3YOURMIND/drf-payload-customizer.svg?style=social&label=Stars)](https://github.com/3YOURMIND/drf-payload-customizer/stargazers)


# drf-payload-customizer
This package allows you to customize your `django-rest-framework` serializer i/o to make modern frontend frameworks happy.

## Requirements
The `mixin` requires you to have the following dependencies:
```
djangorestframework==3.8.2
inflection==0.3.1
```
However, you will require `Django==2.1.2` to run the unit tests. 

## Use it in your project
```
from drf_payload_customizer.mixins import PayloadCustomizationMixin

class CustomTestModelSerializer(PayloadCustomizationMixin, ModelSerializer):
    class Meta:
        model = TestModel
        fields = ('parama', 'param_b',)
        field_mappings = {
            'parama': 'paramA'
        }
```

## To run tests 
```
$ cd drf_payload_customizer
# Make sure you change to a virutal environment according to your project setup
$ python setup.py install 
$ pip install -r requirements.txt 
$ cd tests/test_app/ 
$ python manage.py test 
``` 
