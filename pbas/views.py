from rest_framework import generics, permissions
from .models import TeachingEntry
from .serializers import TeachingEntrySerializer

class TeachingEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = TeachingEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TeachingEntry.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TeachingEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeachingEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TeachingEntry.objects.filter(user=self.request.user)

from .models import StudentSupportEntry, ResearchEntry, AcademicContribution, InstitutionalResponsibility
from .serializers import StudentSupportSerializer, ResearchSerializer, AcademicContributionSerializer, InstitutionalResponsibilitySerializer

class StudentSupportListCreateView(generics.ListCreateAPIView):
    # ... (no change in body)
    serializer_class = StudentSupportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudentSupportEntry.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StudentSupportDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSupportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudentSupportEntry.objects.filter(user=self.request.user)

class ResearchListCreateView(generics.ListCreateAPIView):
    serializer_class = ResearchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResearchEntry.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ResearchDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResearchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ResearchEntry.objects.filter(user=self.request.user)

class AcademicContributionListCreateView(generics.ListCreateAPIView):
    serializer_class = AcademicContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AcademicContribution.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AcademicContributionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AcademicContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AcademicContribution.objects.filter(user=self.request.user)

class InstitutionalResponsibilityListCreateView(generics.ListCreateAPIView):
    serializer_class = InstitutionalResponsibilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InstitutionalResponsibility.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InstitutionalResponsibilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstitutionalResponsibilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InstitutionalResponsibility.objects.filter(user=self.request.user)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Q

class PBASSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        academic_year = request.query_params.get('academic_year')

        teaching_qs = TeachingEntry.objects.filter(user=user)
        support_qs = StudentSupportEntry.objects.filter(user=user)
        research_qs = ResearchEntry.objects.filter(user=user)
        academic_qs = AcademicContribution.objects.filter(user=user)
        institutional_qs = InstitutionalResponsibility.objects.filter(user=user)

        if academic_year:
            teaching_qs = teaching_qs.filter(academic_year=academic_year)
            support_qs = support_qs.filter(academic_year=academic_year)
            research_qs = research_qs.filter(academic_year=academic_year)
            academic_qs = academic_qs.filter(academic_year=academic_year)
            institutional_qs = institutional_qs.filter(academic_year=academic_year)

        teaching_score = round(teaching_qs.aggregate(Sum('score'))['score__sum'] or 0.0, 2)
        support_score = round(support_qs.aggregate(Sum('score'))['score__sum'] or 0.0, 2)
        research_score = round(research_qs.aggregate(Sum('score'))['score__sum'] or 0.0, 2)
        academic_score = round(academic_qs.aggregate(Sum('score'))['score__sum'] or 0.0, 2)
        institutional_score = round(institutional_qs.aggregate(Sum('score'))['score__sum'] or 0.0, 2)

        total_score = round(teaching_score + support_score + research_score + academic_score + institutional_score, 2)
        annual_target = 150.0
        target_percentage = min(100.0, round((total_score / annual_target) * 100, 1))

        # Evidence Health Analysis
        t_total = teaching_qs.count()
        t_evidence = teaching_qs.exclude(Q(supporting_image='') | Q(supporting_image__isnull=True)).count()

        s_total = support_qs.count()
        s_evidence = support_qs.exclude(Q(supporting_image='') | Q(supporting_image__isnull=True)).count()

        r_total = research_qs.count()
        r_evidence = research_qs.exclude(Q(supporting_image='') | Q(supporting_image__isnull=True)).count()

        a_total = academic_qs.count()
        a_evidence = academic_qs.exclude(Q(supporting_image='') | Q(supporting_image__isnull=True)).count()

        i_total = institutional_qs.count()
        i_evidence = institutional_qs.exclude(Q(supporting_image='') | Q(supporting_image__isnull=True)).count()

        total_entries = t_total + s_total + r_total + a_total + i_total
        entries_with_evidence = t_evidence + s_evidence + r_evidence + a_evidence + i_evidence
        evidence_percentage = round((entries_with_evidence / total_entries * 100), 1) if total_entries > 0 else 100.0

        return Response({
            'annual_target': annual_target,
            'total_score': total_score,
            'target_percentage': target_percentage,
            'category_scores': {
                'teaching': {'score': teaching_score, 'max': 25.0, 'count': t_total},
                'student_support': {'score': support_score, 'max': 15.0, 'count': s_total},
                'research': {'score': research_score, 'max': 60.0, 'count': r_total},
                'academic_contributions': {'score': academic_score, 'max': 25.0, 'count': a_total},
                'institutional_responsibilities': {'score': institutional_score, 'max': 25.0, 'count': i_total},
            },
            'evidence_health': {
                'total_entries': total_entries,
                'entries_with_evidence': entries_with_evidence,
                'evidence_percentage': evidence_percentage,
            }
        })

