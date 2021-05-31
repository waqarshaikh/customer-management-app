from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):
    contact = serializers.ReadOnlyField(source='contact.name')
    employee = serializers.ReadOnlyField(source='employee.name')

    def get_contact(self, lead):
        return lead.contact.name

    def get_employee(self, lead):
        return lead.employee.name

    class Meta:
        model = Lead
        fields = ('id', 'contact', 'employee', 'source', 'status', 'id')