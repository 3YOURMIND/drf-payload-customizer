from drf_payload_customizer.mixins.payload_no_null_or_none_mixin import \
    PayloadNoNullOrNoneMixin
from drf_payload_customizer.mixins.payload_transformation_mixin import \
    PayloadTransformationMixin
from drf_payload_customizer.mixins.payload_translation_mixin import \
    PayloadTranslationMixin


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
