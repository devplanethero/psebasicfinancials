from rest_framework.serializers import ModelSerializer,CharField
from .models import EconomicIndicatorRecord, Indicator, Country

class IndicatorSerializer(ModelSerializer):
    class Meta:
        model = Indicator
        fields = '__all__'

class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class EconomicIndicatorRecordSerializer(ModelSerializer):
    economic_indicator_title = CharField(source="economic_indicator.title")
    country_name= CharField(source="country.name")

    class Meta:
        model = EconomicIndicatorRecord
        fields = [
            'economic_indicator_title',
            'country_name',
            'year',
            'quarter',
            'period',
            'value'
        ]