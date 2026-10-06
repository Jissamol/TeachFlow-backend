from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    TeachingEntry, StudentSupportEntry, ResearchEntry, 
    AcademicContribution, InstitutionalResponsibility,
    ScoringRule, AppraisalPeriod, ActivityEvidence, Notification
)
from .serializers import (
    TeachingEntrySerializer, StudentSupportSerializer, ResearchSerializer, 
    AcademicContributionSerializer, InstitutionalResponsibilitySerializer,
    ScoringRuleSerializer, AppraisalPeriodSerializer, ActivityEvidenceSerializer,
    NotificationSerializer
)


class ScoringRuleListCreateView(generics.ListCreateAPIView):
    queryset = ScoringRule.objects.all()
    serializer_class = ScoringRuleSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScoringRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ScoringRule.objects.all()
    serializer_class = ScoringRuleSerializer
    permission_classes = [permissions.IsAuthenticated]

class AppraisalPeriodListCreateView(generics.ListCreateAPIView):
    serializer_class = AppraisalPeriodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AppraisalPeriod.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AppraisalPeriodDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppraisalPeriodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AppraisalPeriod.objects.filter(user=self.request.user)

class ActivityEvidenceListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivityEvidenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = ActivityEvidence.objects.filter(user=self.request.user).order_by('-upload_date')
        year = self.request.query_params.get('academic_year')
        if year:
            qs = qs.filter(academic_year=year)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityEvidenceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivityEvidenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActivityEvidence.objects.filter(user=self.request.user)

class TeachingEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = TeachingEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = TeachingEntry.objects.filter(user=self.request.user).order_by('-created_at')
        year = self.request.query_params.get('academic_year')
        if year:
            qs = qs.filter(academic_year=year)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TeachingEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeachingEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TeachingEntry.objects.filter(user=self.request.user)

class StudentSupportListCreateView(generics.ListCreateAPIView):
    serializer_class = StudentSupportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = StudentSupportEntry.objects.filter(user=self.request.user).order_by('-created_at')
        year = self.request.query_params.get('academic_year')
        if year:
            qs = qs.filter(academic_year=year)
        return qs

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
        qs = ResearchEntry.objects.filter(user=self.request.user).order_by('-created_at')
        year = self.request.query_params.get('academic_year')
        if year:
            qs = qs.filter(academic_year=year)
        return qs

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
        qs = AcademicContribution.objects.filter(user=self.request.user).order_by('-created_at')
        year = self.request.query_params.get('academic_year')
        if year:
            qs = qs.filter(academic_year=year)
        return qs

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
        qs = InstitutionalResponsibility.objects.filter(user=self.request.user).order_by('-created_at')
        year = self.request.query_params.get('academic_year')
        if year:
            qs = qs.filter(academic_year=year)
        return qs

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
        academic_year = request.query_params.get('academic_year', 'All')

        appraisal, created = AppraisalPeriod.objects.get_or_create(
            user=user,
            academic_year=academic_year if academic_year != 'All' else '2025-2026',
            defaults={
                'title': f"{academic_year} Annual Appraisal",
                'target_score': 300.0,
                'status': 'Draft'
            }
        )

        teaching_qs = TeachingEntry.objects.filter(user=user)
        support_qs = StudentSupportEntry.objects.filter(user=user)
        research_qs = ResearchEntry.objects.filter(user=user)
        academic_qs = AcademicContribution.objects.filter(user=user)
        institutional_qs = InstitutionalResponsibility.objects.filter(user=user)
        evidence_qs = ActivityEvidence.objects.filter(user=user)

        if academic_year and academic_year != 'All':
            year_prefix = academic_year.split('-')[0]
            year_filter = Q(academic_year=academic_year) | Q(academic_year__startswith=year_prefix)
            teaching_qs = teaching_qs.filter(year_filter)
            support_qs = support_qs.filter(year_filter)
            research_qs = research_qs.filter(year_filter)
            academic_qs = academic_qs.filter(year_filter)
            institutional_qs = institutional_qs.filter(year_filter)
            evidence_qs = evidence_qs.filter(year_filter)

        teaching_score = round(teaching_qs.aggregate(Sum('score'))['score__sum'] or 0.0, 2)
        support_score = round(support_qs.aggregate(Sum('score'))['score__sum'] or 0.0, 2)
        research_score = round(research_qs.aggregate(Sum('score'))['score__sum'] or 0.0, 2)
        academic_score = round(academic_qs.aggregate(Sum('score'))['score__sum'] or 0.0, 2)
        institutional_score = round(institutional_qs.aggregate(Sum('score'))['score__sum'] or 0.0, 2)

        total_score = round(teaching_score + support_score + research_score + academic_score + institutional_score, 2)
        annual_target = appraisal.target_score
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
        entries_with_evidence = t_evidence + s_evidence + r_evidence + a_evidence + i_evidence + evidence_qs.count()
        evidence_percentage = min(100.0, round((entries_with_evidence / max(1, total_entries) * 100), 1)) if total_entries > 0 else 100.0

        rules = ScoringRule.objects.all()
        rules_list = [{'activity_type': r.activity_type, 'points': r.points_per_unit, 'is_per_hour': r.is_per_hour} for r in rules]

        return Response({
            'academic_year': academic_year,
            'appraisal_period': {
                'id': appraisal.id,
                'title': appraisal.title,
                'status': appraisal.status,
                'target_score': appraisal.target_score,
                'period_start': appraisal.period_start,
                'period_end': appraisal.period_end,
            },
            'annual_target': annual_target,
            'total_score': total_score,
            'target_percentage': target_percentage,
            'category_scores': {
                'teaching': {'score': teaching_score, 'count': t_total},
                'student_support': {'score': support_score, 'count': s_total},
                'research': {'score': research_score, 'count': r_total},
                'academic_contributions': {'score': academic_score, 'count': a_total},
                'institutional_responsibilities': {'score': institutional_score, 'count': i_total},
            },
            'evidence_health': {
                'total_entries': total_entries,
                'entries_with_evidence': entries_with_evidence,
                'evidence_percentage': evidence_percentage,
                'total_evidence_files': evidence_qs.count(),
                'category_breakdown': {
                    'teaching': {'verified': t_evidence, 'missing': max(0, t_total - t_evidence)},
                    'student_support': {'verified': s_evidence, 'missing': max(0, s_total - s_evidence)},
                    'research': {'verified': r_evidence, 'missing': max(0, r_total - r_evidence)},
                    'academic': {'verified': a_evidence, 'missing': max(0, a_total - a_evidence)},
                    'institutional': {'verified': i_evidence, 'missing': max(0, i_total - i_evidence)},
                }
            },
            'scoring_rules': rules_list
        })


class NotificationListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def sync_system_notifications(self, user):
        # 1. Incomplete Evidence Notification
        t_missing = TeachingEntry.objects.filter(user=user, supporting_image__in=['', None]).count()
        s_missing = StudentSupportEntry.objects.filter(user=user, supporting_image__in=['', None]).count()
        r_missing = ResearchEntry.objects.filter(user=user, supporting_image__in=['', None]).count()
        a_missing = AcademicContribution.objects.filter(user=user, supporting_image__in=['', None]).count()
        i_missing = InstitutionalResponsibility.objects.filter(user=user, supporting_image__in=['', None]).count()
        missing_count = t_missing + s_missing + r_missing + a_missing + i_missing

        if missing_count > 0:
            Notification.objects.update_or_create(
                user=user,
                notification_type='Evidence',
                defaults={
                    'title': 'Incomplete evidence',
                    'message': f'{missing_count} activities are missing supporting documents.',
                    'icon': '🔔',
                    'action_url': '/pbas/evidence'
                }
            )

        # 2. Goal Progress Notification
        t_score = sum(e.score for e in TeachingEntry.objects.filter(user=user))
        s_score = sum(e.score for e in StudentSupportEntry.objects.filter(user=user))
        r_score = sum(e.score for e in ResearchEntry.objects.filter(user=user))
        a_score = sum(e.score for e in AcademicContribution.objects.filter(user=user))
        i_score = sum(e.score for e in InstitutionalResponsibility.objects.filter(user=user))
        total_score = round(t_score + s_score + r_score + a_score + i_score, 2)
        target = 300.0
        pct = min(100, int((total_score / target) * 100))

        Notification.objects.update_or_create(
            user=user,
            notification_type='Goal',
            defaults={
                'title': 'Goal progress',
                'message': f'You have completed {pct}% of your annual research target.',
                'icon': '🔔',
                'action_url': '/pbas/dashboard'
            }
        )

        # 3. Appraisal Deadline Approaching Notification
        Notification.objects.get_or_create(
            user=user,
            notification_type='Deadline',
            defaults={
                'title': 'Appraisal deadline approaching',
                'message': 'Your 2025–26 appraisal submission deadline is in 7 days.',
                'icon': '🔔',
                'action_url': '/pbas/reports'
            }
        )

    def get(self, request):
        self.sync_system_notifications(request.user)
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        unread_count = notifications.filter(is_read=False).count()
        return Response({
            'notifications': serializer.data,
            'unread_count': unread_count
        })

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class NotificationMarkReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            notif = Notification.objects.get(pk=pk, user=request.user)
            notif.is_read = True
            notif.save()
            return Response({'status': 'marked read'})
        except Notification.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)


class NotificationMarkAllReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Notification.objects.filter(user=request.user).update(is_read=True)
        return Response({'status': 'all marked read'})


class NotificationDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


