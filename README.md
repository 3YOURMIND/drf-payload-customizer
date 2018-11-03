# drf-payload-customizer

[![License](https://img.shields.io/github/license/3yourmind/drf-payload-customizer.svg)](./LICENSE)
[![Contributing](https://img.shields.io/badge/PR-welcome-green.svg)](https://github.com/3YOURMIND/drf-payload-customizer/pulls)
[![3yourminD-Careers](https://img.shields.io/badge/3YOURMIND-Hiring-brightgreen.svg)](https://www.3yourmind.com/career)
[![Stars](https://img.shields.io/github/stars/3YOURMIND/drf-payload-customizer.svg?style=social&label=Stars)](https://github.com/3YOURMIND/drf-payload-customizer/stargazers)

This package allows you to customize your `django-rest-framework` serializer i/o to make modern frontend frameworks happy.
The following modifications are supported: 
1. **Transformation**: Convert all `keys` in API output to `camelCase`. Also
 on reception of an input on an API, transform all inputs to `snake_case`. 
2. **Translation**: Rename a `key` in your API schema. (works in both 
direction). 
3. **Nullify/Balankify**: Replace `""` with `None` on output direction and 
vice versa in the other direction. 

We introduce 3 seperate `Mixins` that can you can subclass your `APIView` 
from to achieve 1-3. They are: 
1. `PayloadTransformationMixin`: Perform transformation (1) above. Has an 
optional parameter `PAYLOAD_TRANSFORM_NESTED` (see tests) which you can set 
to `True` in your `Serializer.Meta` class to recursively convert all nested 
dictionaries. This feature only works in the output direction. 
2. `PayloadTranslationMixin`: Perform translation (2) above. You can specify
 custom mappings using a `field_mappings` dict in your `Serializer.Meta` 
 class.
3. `PayloadNoNullOrNoneMixin`: Perform nullify/blankify (3) above.  

## Requirements
The `mixin` requires you to have the following dependencies:
```
djangorestframework==3.8.2
```
We are positive it would work with other versions of Django Rest Framework 
as well. However, you will require `Django==2.1.2` to run the unit tests. 

## Use it in your project

You can use all three of the mixins together like this in your project using
our `drf_payload_customizer.mixins.PayloadConverterMixin` mixin. The mixin 
performs (1-3) modifications listed above. Here is how it is implemented:
```
class PayloadConverterMixin(PayloadTransformationMixin,
                            PayloadTranslationMixin,
                            PayloadNoNullOrNoneMixin):
    """
    Use this mixin in all of our Serializers, to convert the JSON into a
    format that is easier consumed by modern front-ends.
    """

    def to_representation(self, instance):
        return super().to_representation(instance)

    def to_internal_value(self, camel_cased):
        return super().to_internal_value(camel_cased)
``` 
Now, subclass your `APIViews` with `PayloadConverterMixin` as given below:

```
from drf_payload_customizer.mixins import PayloadConverterMixin

class CustomTestModelSerializer(PayloadConverterMixin, ModelSerializer):
    class Meta:
        model = TestModel
        fields = ('parama', 'param_b',)
        PAYLOAD_TRANSFORM_NESTED = True
        # The mapping is the snake_case of your expected o/p
        field_mappings = {
            'parama': 'param_a' 
        }
        
# Now your serializer would output: 
test_serializer = CustomTestModelSerializer(obj)
JSONRenderer().render(test_serializer.data)
> {'paramA': '', 'paramB': None}

# Your serializer also admits input in the same format: 
content = json.dumps({'paramA': 'testA', 'paramB': 3}).encode()
stream = BytesIO(content)
data = JSONParser().parse(stream)
serializer = CustomTestModelSerializer(data=data)
self.assertTrue(serializer.is_valid())
> True
```

## To run tests 

```sh
cd drf_payload_customizer
# Make sure you change to a virutal environment according to your project setup
python setup.py install 
pip install -r requirements.txt 
cd tests/test_app/ 
python manage.py test 
``` 
