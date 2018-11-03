from collections import OrderedDict

from rest_framework import fields


class PayloadNoNullOrNoneMixin:
    """
    This mixin converts: "" => to null during Python to JSON and null => ""
    while accepting data from JSON
    """
    @staticmethod
    def _is_charfield(field):
        """
        @TODO: Improve this to check fields shadowed by Charfield
        """
        return isinstance(field, fields.CharField)

    @staticmethod
    def _nullify(value):
        return None if value == "" else value

    @staticmethod
    def _blankify(value):
        return "" if value is None else value

    def _nullify_dict(self, dictionary) -> dict:
        nullified_dict = {}

        for key, value in dictionary.items():
            is_dict = isinstance(value, dict)
            nullified_dict[key] = \
                self._nullify_dict(value) if is_dict else self._nullify(value)

        return nullified_dict

    def to_internal_value(self, payload: OrderedDict):
        for key, value in payload.items():
            is_character_field = self._is_charfield(
                self.fields.get(key)
            )
            payload[key] = (
                self._blankify(value) if is_character_field else value
            )
        return super().to_internal_value(payload)

    def to_representation(self, instance) -> dict:
        snake_cased = super().to_representation(instance)
        return self._nullify_dict(snake_cased)
