# drf-payload-customizer
This package allows you to customize your `django-rest-framework` serializer i/o to make modern frontend frameworks happy.

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
