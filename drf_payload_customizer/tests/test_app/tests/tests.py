import json
from django.db import models
from django.test import TestCase
from django.utils.six import BytesIO


from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.serializers import ModelSerializer

from drf_payload_customizer.mixins import PayloadCustomizationMixin


class TestModel(models.Model):
    parama = models.CharField(max_length=5, blank=True)
    param_b = models.IntegerField()


class CustomTestModelSerializer(PayloadCustomizationMixin, ModelSerializer):
    class Meta:
        model = TestModel
        fields = ('parama', 'param_b',)
        field_mappings = {
            'parama': 'paramA'
        }


class NestedTestModelSerializer(PayloadCustomizationMixin,
                                serializers.ModelSerializer):
    param_c = serializers.SerializerMethodField()

    def get_param_c(self, instance):
        return {
            'key': 'value',
            'key_snake': 'value_snake',
            'keyCamel': 'valueCamel'
        }

    class Meta:
        model = TestModel
        fields = ('parama', 'param_b', 'param_c',)
        field_mappings = {
            'parama': 'paramA'
        }


class PayloadConverterMixinTest(TestCase):
    def setUp(self):
        super().setUp()

    def test_read_works_on_mapped_fields(self):
        test_object = TestModel()
        test_serializer = CustomTestModelSerializer(test_object)
        serialized_data = JSONRenderer().render(test_serializer.data)
        self.assertEquals({'paramA': '', 'paramB': None},
                          json.loads(serialized_data))

    def test_write_works_on_mapped_fields(self):
        content = json.dumps(
            {
                'paramA': 'testA',
                'paramB': 3
            }
        ).encode()
        stream = BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = CustomTestModelSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_payload_conversion_with_nested_fields(self):
        test_object = TestModel()
        test_serializer = NestedTestModelSerializer(test_object)
        serialized_data = JSONRenderer().render(test_serializer.data)
        self.assertEquals(
            {'paramA': '', 'paramB': None,
             'paramC': {'key': 'value', 'keySnake': 'value_snake',
                        'keyCamel': 'valueCamel'}},
            json.loads(serialized_data)
        )
