from collections import Mapping
import re

from rest_framework.settings import api_settings
from rest_framework.serializers import ValidationError
from rest_framework.utils.serializer_helpers import ReturnDict


class PayloadTransformationMixin:
    """
    This mixin converts python snake_case fields into
    camelCase JSON. This works for serialization and deserialization.
    """
    @staticmethod
    def _do_transform_to_internal_value(camel_key):
        snake_cased = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', camel_key)
        snake_cased = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', snake_cased)
        return snake_cased.lower()

    def transform_to_internal_value(self, camel_cased):
        fields_dict = {}
        for camel_key, value in camel_cased.items():
            transformed_key = self._do_transform_to_internal_value(camel_key)
            fields_dict[transformed_key] = value

        return fields_dict

    def to_internal_value(self, camel_cased):
        if not isinstance(camel_cased, Mapping):
            message = self.error_messages['invalid'].format(
                datatype=type(camel_cased).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='invalid')
        return super().to_internal_value(
            self.transform_to_internal_value(camel_cased)
        )

    @staticmethod
    def _do_transform_to_representation(snake_key):
        first_letter = snake_key[0].lower()
        rest = re.sub(r'(?:^|_)(.)', lambda x: x.group(1).upper(),
                      snake_key)[1:]
        return f'{first_letter}{rest}'

    def transform_to_representation(self, snake_cased):
        fields_dict = {}
        transform_needed = getattr(
            getattr(self, 'Meta', None), 'PAYLOAD_TRANSFORM_NESTED', False)

        for key, value in snake_cased.items():
            transformed_key = self._do_transform_to_representation(key)
            fields_dict[transformed_key] = value

            if transform_needed and isinstance(value, dict):
                fields_dict[transformed_key] = \
                    self.transform_to_representation(value)

        return fields_dict

    def to_representation(self, instance):
        return self.transform_to_representation(
            super().to_representation(instance)
        )

    @property
    def errors(self):
        ret = self.transform_to_representation(super().errors)
        return ReturnDict(ret, serializer=self)
