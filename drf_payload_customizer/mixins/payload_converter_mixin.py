import inflection

from rest_framework.utils.serializer_helpers import ReturnDict


class PayloadCustomizationMixin:
    """
    This mixin does the following:
    1) Transformation:
        - Convert snake_cased to camelCased in response
        - Convert camelCased to snake_cased while accepting a request
        To enable: Simply add the fields in your fields = tuple in your
        serializer Meta class.
    2) Translations (for ModelSerializer):
        - Use a custom key for your model field
        To enable: Add the following to your ModelSerializer.Meta class
        class YourModelSerializer(PayloadCustomizationMixin,
                                serializers.ModelSerializer):
            class Meta:
                field_mappings = {
                    'model_key_a': 'modifiedKeyA',
                    'model_key_b': 'modifiedKeyB',
                }
                fields = ('model_key_a', 'model_key_b',)

        Note: the mapped fields are not further transformed. Your
        serializers would now accept the value for a translated field using
        its filed_mapping as well
    To use the mixin, create your serializer class inheriting
    PayloadCustomizationMixin before others (say ModelSerializer)
    """

    def _do_translate_to_internal_value(self, mapped_field):
        reverse_field_mapping = dict(
            (value, key) for key, value in self.Meta.field_mappings.items()
        )
        return reverse_field_mapping.get(mapped_field, None)

    @staticmethod
    def _do_transform_to_internal_value(camel_key):
        return inflection.underscore(camel_key)

    def translate_or_transform_to_internal_value(self, camel_cased):
        fields_dict = {}
        field_mappings = getattr(
            getattr(self, 'Meta', None), 'field_mappings', {})

        for key, value in camel_cased.items():
            if key not in field_mappings.values():
                transformed_key = self._do_transform_to_internal_value(key)
            else:
                transformed_key = self._do_translate_to_internal_value(key)

            fields_dict[transformed_key] = value
            if isinstance(value, dict):
                fields_dict[transformed_key] = \
                    self.translate_or_transform_to_internal_value(value)

        return fields_dict

    def to_internal_value(self, camel_cased):
        return super().to_internal_value(
            self.translate_or_transform_to_internal_value(camel_cased)
        )

    def _do_translate_to_representation(self, mapped_key):
        return self.Meta.field_mappings[mapped_key]

    @staticmethod
    def _do_transform_to_representation(snake_key):
        return inflection.camelize(
            str(snake_key), uppercase_first_letter=False
        )

    def translate_or_transform_to_representation(self, snake_cased):
        fields_dict = {}
        field_mappings = getattr(
            getattr(self, 'Meta', None), 'field_mappings', {})

        for snake_key, value in snake_cased.items():
            if snake_key not in field_mappings.keys():
                transformed_key = self._do_transform_to_representation(
                    snake_key
                )
            else:
                transformed_key = self._do_translate_to_representation(
                    snake_key
                )

            fields_dict[transformed_key] = value
            if isinstance(value, dict):
                fields_dict[transformed_key] = \
                    self.translate_or_transform_to_representation(value)

        return fields_dict

    def to_representation(self, instance):
        snake_cased = super().to_representation(instance)
        return self.translate_or_transform_to_representation(snake_cased)

    @property
    def errors(self):
        ret = self.translate_or_transform_to_representation(super().errors)
        return ReturnDict(ret, serializer=self)
