from rest_framework import serializers
from .models import TeachingEntry

class TeachingEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingEntry
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

from .models import StudentSupportEntry, ResearchEntry, AcademicContribution, InstitutionalResponsibility

class StudentSupportSerializer(serializers.ModelSerializer):
    # ... (no change)
    class Meta:
        model = StudentSupportEntry
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class ResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchEntry
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class AcademicContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicContribution
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class InstitutionalResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionalResponsibility
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
