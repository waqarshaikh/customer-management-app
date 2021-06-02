from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):
    company = serializers.ReadOnlyField(source='company.company_name')
    employee = serializers.ReadOnlyField(source='employee.name')

    def get_company(self, lead):
        return lead.company.company_name

    def get_employee(self, lead):
        return lead.employee.name

    class Meta:
        model = Lead
        fields = ('id', 'company', 'employee', 'source', 'status', 'id')