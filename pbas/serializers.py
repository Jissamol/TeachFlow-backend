from rest_framework import serializers
from .models import (
    TeachingEntry, StudentSupportEntry, ResearchEntry, 
    AcademicContribution, InstitutionalResponsibility,
    ScoringRule, AppraisalPeriod, ActivityEvidence
)

class ScoringRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoringRule
        fields = '__all__'

class AppraisalPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppraisalPeriod
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

class ActivityEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityEvidence
        fields = '__all__'
        read_only_fields = ['user', 'upload_date']

class TeachingEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingEntry
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class StudentSupportSerializer(serializers.ModelSerializer):
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
