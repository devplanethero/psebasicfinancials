from rest_framework.serializers import ModelSerializer,CharField
from base.models import Financials, Company, Industry

class FinancialsSerializer(ModelSerializer):
    class Meta:
        model = Financials
        fields = '__all__'

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class IndustrySerializer(ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'

class SelectedFinancialsSerializer(ModelSerializer):
    ticker_type = CharField(source="ticker.type")
    ticker= CharField(source="ticker.ticker")
    ticker_name = CharField(source="ticker.name")

    class Meta:
        model = Financials
        fields = [
            'Total_Assets',
            'Total_Net_Income',
            'ticker',
            'ticker_name',
            'period',
            'quarter',
            'reporting_period',
            'year',
            'ticker_type'
        ]

        # depth=1