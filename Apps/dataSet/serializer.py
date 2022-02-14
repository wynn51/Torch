from rest_framework import serializers
from .models import *


class DataRulesSerializers(serializers.ModelSerializer):
    class Meta:
        model = DataRules
        fields = ['id', 'indicator_name', 'indicator_unit', 'indicator_code', 'indicator_address', 'indicator_type', 'dynamicFormula']
        # extra_kwargs = {
        #
        # }
