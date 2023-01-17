from rest_framework.serializers import ModelSerializer
from base.models import Financials, Company


class FinancialsSerializer(ModelSerializer):
    class Meta:
        model = Financials
        fields = '__all__'

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'