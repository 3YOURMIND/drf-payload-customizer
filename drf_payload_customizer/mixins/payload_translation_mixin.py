class PayloadTranslationMixin:
    """
    This mixin supports custom field mappings via an
    array 'field_mappings': {'field': 'custom_name'} property in
    Serializer.Meta. Always supply the snake_case version as a mapping.
    """

    def _do_translate_to_internal_value(self, mapped_field):
        reverse_field_mapping = dict(
            (value, key) for key, value in self.Meta.field_mappings.items()
        )
        return reverse_field_mapping.get(mapped_field, None)

    def translate_to_internal_value(self, payload):
        fields_dict = {}
        field_mappings = getattr(
            getattr(self, 'Meta', None), 'field_mappings', {})

        for key, value in payload.items():
            if key in field_mappings.values():
                key = self._do_translate_to_internal_value(key)

            fields_dict[key] = value

        return fields_dict

    def to_internal_value(self, camel_cased):
        return super().to_internal_value(
            self.translate_to_internal_value(camel_cased)
        )

    def _do_translate_to_representation(self, mapped_key):
        return self.Meta.field_mappings[mapped_key]

    def translate_to_representation(self, payload):
        fields_dict = {}
        field_mappings = getattr(
            getattr(self, 'Meta', None), 'field_mappings', {})

        for key, value in payload.items():
            if key in field_mappings.keys():
                key = self._do_translate_to_representation(key)

            fields_dict[key] = value

        return fields_dict

    def to_representation(self, instance):
        return self.translate_to_representation(
            super().to_representation(instance))
