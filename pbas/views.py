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


from datetime import date as datetime_date

class CalendarEventsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def seed_default_events(self, user):
        if not StudentSupportEntry.objects.filter(user=user, academic_year='2026-2027').exists() and \
           not ResearchEntry.objects.filter(user=user, academic_year='2026-2027').exists() and \
           not AcademicContribution.objects.filter(user=user, academic_year='2026-2027').exists() and \
           not InstitutionalResponsibility.objects.filter(user=user, academic_year='2026-2027').exists():
            
            # 🟢 Workshop
            StudentSupportEntry.objects.create(
                user=user,
                academic_year='2026-2027',
                activity_name='AI & Data Analytics Workshop',
                description='Hands-on workshop for undergraduate students on Machine Learning and Data Science tools.',
                target_audience='UG & PG Computer Science Students',
                hours_spent=15,
                from_date='2026-10-08',
                to_date='2026-10-08'
            )
            StudentSupportEntry.objects.create(
                user=user,
                academic_year='2026-2027',
                activity_name='Student Career Guidance & Mentorship Seminar',
                description='Interactive session on higher education, placements, and research career pathways.',
                target_audience='Final Year Students',
                hours_spent=10,
                from_date='2026-10-20',
                to_date='2026-10-20'
            )

            # 🔵 Conference
            AcademicContribution.objects.create(
                user=user,
                academic_year='2026-2027',
                contribution_type='Paper Presentation',
                title='Optimization of Neural Networks in Edge Computing',
                event_name='International Conference on Intelligent Systems (ICIS 2026)',
                organization='IEEE Computer Society',
                date='2026-10-12',
                from_date='2026-10-12',
                to_date='2026-10-13',
                description='Presented research paper on lightweight neural network deployment for edge devices.'
            )
            AcademicContribution.objects.create(
                user=user,
                academic_year='2026-2027',
                contribution_type='Resource Person',
                title='Keynote: Next Generation Cyber Security Protocols',
                event_name='National Cyber Security Summit 2026',
                organization='Department of Computer Science & IIT Madras',
                date='2026-10-29',
                from_date='2026-10-29',
                to_date='2026-10-29',
                description='Delivered keynote speech on modern encryption standards and privacy models.'
            )

            # 🟣 Lecture
            TeachingEntry.objects.create(
                user=user,
                academic_year='2026-2027',
                course_name='Advanced Distributed Systems (CS801)',
                course_level='PG',
                mode_of_teaching='Lecture',
                classes_assigned=40,
                classes_taught=38,
                from_date='2026-10-05',
                to_date='2026-10-05',
                description='Special guest lecture series on consensus algorithms (Raft & Paxos).'
            )
            AcademicContribution.objects.create(
                user=user,
                academic_year='2026-2027',
                contribution_type='Invited Lecture',
                title='Invited Talk on Deep Reinforcement Learning',
                event_name='State University Faculty Development Program',
                organization='State University Department of IT',
                date='2026-10-27',
                from_date='2026-10-27',
                to_date='2026-10-27',
                description='Special session on Reinforcement Learning architectures for AI faculty.'
            )

            # 🟠 Research
            ResearchEntry.objects.create(
                user=user,
                academic_year='2026-2027',
                research_type='Journal',
                title='Scalable Federated Learning in Heterogeneous Medical Datasets',
                journal_or_funding='IEEE Transactions on Knowledge and Data Engineering',
                status_or_impact='Impact Factor: 8.9 (Published)',
                from_date='2026-10-16',
                to_date='2026-10-16',
                description='Peer-reviewed journal publication detailing novel privacy-preserving ML algorithms.'
            )

            # 🔴 Institutional Duty
            InstitutionalResponsibility.objects.create(
                user=user,
                academic_year='2026-2027',
                responsibility_type='Administrative',
                position='IQAC Quality Coordinator & Academic Auditor',
                description='Internal quality audit and documentation review for NAAC accreditation standards.',
                from_date='2026-10-02',
                to_date='2026-10-02'
            )
            InstitutionalResponsibility.objects.create(
                user=user,
                academic_year='2026-2027',
                responsibility_type='Examination',
                position='Chief Superintendent of Semester End Examinations',
                description='Overseeing university end-semester examination logistics and valuation center.',
                from_date='2026-10-23',
                to_date='2026-10-23'
            )

    def get(self, request):
        user = request.user
        self.seed_default_events(user)

        events = []

        # 1. Student Support / Workshop (🟢 Workshop)
        for e in StudentSupportEntry.objects.filter(user=user):
            event_date = e.from_date or (e.created_at.date() if e.created_at else None)
            if event_date:
                events.append({
                    'id': f'support-{e.id}',
                    'db_id': e.id,
                    'type': 'Student Support',
                    'category': 'Workshop',
                    'category_label': '🟢 Workshop',
                    'color': '#10b981',
                    'bg_light': 'rgba(16, 185, 129, 0.15)',
                    'title': e.activity_name,
                    'date': str(event_date),
                    'score': e.score,
                    'description': e.description or f'Target Audience: {e.target_audience}, Hours: {e.hours_spent}',
                    'target_audience': e.target_audience,
                    'hours_spent': e.hours_spent,
                    'academic_year': e.academic_year,
                    'has_evidence': bool(e.supporting_image),
                    'url': '/pbas/student-support'
                })

        # 2. Teaching Entry (🟣 Lecture / 🟢 Workshop)
        for e in TeachingEntry.objects.filter(user=user):
            event_date = e.from_date or (e.created_at.date() if e.created_at else None)
            if event_date:
                is_workshop = 'workshop' in (e.course_name + ' ' + (e.description or '')).lower()
                cat = 'Workshop' if is_workshop else 'Lecture'
                cat_label = '🟢 Workshop' if is_workshop else '🟣 Lecture'
                color = '#10b981' if is_workshop else '#a855f7'
                bg_light = 'rgba(16, 185, 129, 0.15)' if is_workshop else 'rgba(168, 85, 247, 0.15)'

                events.append({
                    'id': f'teaching-{e.id}',
                    'db_id': e.id,
                    'type': 'Teaching & Learning',
                    'category': cat,
                    'category_label': cat_label,
                    'color': color,
                    'bg_light': bg_light,
                    'title': e.course_name,
                    'date': str(event_date),
                    'score': e.score,
                    'description': e.description or f'Mode: {e.mode_of_teaching}, Classes Taught: {e.classes_taught}/{e.classes_assigned}',
                    'mode_of_teaching': e.mode_of_teaching,
                    'classes_taught': e.classes_taught,
                    'academic_year': e.academic_year,
                    'has_evidence': bool(e.supporting_image),
                    'url': '/pbas/teaching'
                })

        # 3. Academic Contribution (🔵 Conference / 🟣 Lecture / 🟢 Workshop)
        for e in AcademicContribution.objects.filter(user=user):
            event_date = e.date or e.from_date or (e.created_at.date() if e.created_at else None)
            if event_date:
                t_lower = (e.contribution_type + ' ' + e.title + ' ' + e.event_name).lower()
                if 'conference' in t_lower or 'presentation' in t_lower or 'paper' in t_lower:
                    cat = 'Conference'
                    cat_label = '🔵 Conference'
                    color = '#3b82f6'
                    bg_light = 'rgba(59, 130, 246, 0.15)'
                elif 'lecture' in t_lower or 'talk' in t_lower or 'invited' in t_lower:
                    cat = 'Lecture'
                    cat_label = '🟣 Lecture'
                    color = '#a855f7'
                    bg_light = 'rgba(168, 85, 247, 0.15)'
                else:
                    cat = 'Workshop'
                    cat_label = '🟢 Workshop'
                    color = '#10b981'
                    bg_light = 'rgba(16, 185, 129, 0.15)'

                events.append({
                    'id': f'academic-{e.id}',
                    'db_id': e.id,
                    'type': 'Academic Contribution',
                    'category': cat,
                    'category_label': cat_label,
                    'color': color,
                    'bg_light': bg_light,
                    'title': e.title,
                    'date': str(event_date),
                    'score': e.score,
                    'description': e.description or f'Event: {e.event_name} by {e.organization}',
                    'event_name': e.event_name,
                    'organization': e.organization,
                    'academic_year': e.academic_year,
                    'has_evidence': bool(e.supporting_image),
                    'url': '/pbas/academic'
                })

        # 4. Research Entry (🟠 Research / 🔵 Conference)
        for e in ResearchEntry.objects.filter(user=user):
            event_date = e.from_date or (e.created_at.date() if e.created_at else None)
            if event_date:
                if e.research_type == 'Conference':
                    cat = 'Conference'
                    cat_label = '🔵 Conference'
                    color = '#3b82f6'
                    bg_light = 'rgba(59, 130, 246, 0.15)'
                else:
                    cat = 'Research'
                    cat_label = '🟠 Research'
                    color = '#f97316'
                    bg_light = 'rgba(249, 115, 22, 0.15)'

                events.append({
                    'id': f'research-{e.id}',
                    'db_id': e.id,
                    'type': 'Research',
                    'category': cat,
                    'category_label': cat_label,
                    'color': color,
                    'bg_light': bg_light,
                    'title': e.title,
                    'date': str(event_date),
                    'score': e.score,
                    'description': e.description or f'Journal/Funding: {e.journal_or_funding}, Impact: {e.status_or_impact}',
                    'journal_or_funding': e.journal_or_funding,
                    'status_or_impact': e.status_or_impact,
                    'academic_year': e.academic_year,
                    'has_evidence': bool(e.supporting_image),
                    'url': '/pbas/research'
                })

        # 5. Institutional Responsibility (🔴 Institutional Duty)
        for e in InstitutionalResponsibility.objects.filter(user=user):
            event_date = e.from_date or (e.created_at.date() if e.created_at else None)
            if event_date:
                events.append({
                    'id': f'institutional-{e.id}',
                    'db_id': e.id,
                    'type': 'Institutional Responsibility',
                    'category': 'Institutional Duty',
                    'category_label': '🔴 Institutional Duty',
                    'color': '#ef4444',
                    'bg_light': 'rgba(239, 68, 68, 0.15)',
                    'title': f'{e.position} ({e.responsibility_type})',
                    'date': str(event_date),
                    'score': e.score,
                    'description': e.description,
                    'position': e.position,
                    'responsibility_type': e.responsibility_type,
                    'academic_year': e.academic_year,
                    'has_evidence': bool(e.supporting_image),
                    'url': '/pbas/institutional'
                })

        return Response(events)

    def post(self, request):
        user = request.user
        category = request.data.get('category', 'Workshop')
        title = request.data.get('title', 'New Activity')
        date_str = request.data.get('date', str(datetime_date.today()))
        description = request.data.get('description', '')
        academic_year = request.data.get('academic_year', '2026-2027')

        if category == 'Workshop':
            entry = StudentSupportEntry.objects.create(
                user=user,
                academic_year=academic_year,
                activity_name=title,
                description=description,
                target_audience='Students & Faculty',
                hours_spent=5,
                from_date=date_str,
                to_date=date_str
            )
            created_type = 'student-support'
        elif category == 'Conference':
            entry = AcademicContribution.objects.create(
                user=user,
                academic_year=academic_year,
                contribution_type='Paper Presentation',
                title=title,
                event_name='Academic Conference',
                organization='University Research Cell',
                date=date_str,
                from_date=date_str,
                to_date=date_str,
                description=description
            )
            created_type = 'academic'
        elif category == 'Lecture':
            entry = TeachingEntry.objects.create(
                user=user,
                academic_year=academic_year,
                course_name=title,
                course_level='UG',
                mode_of_teaching='Lecture',
                classes_assigned=10,
                classes_taught=10,
                from_date=date_str,
                to_date=date_str,
                description=description
            )
            created_type = 'teaching'
        elif category == 'Research':
            entry = ResearchEntry.objects.create(
                user=user,
                academic_year=academic_year,
                research_type='Journal',
                title=title,
                journal_or_funding='Academic Journal',
                status_or_impact='Submitted',
                from_date=date_str,
                to_date=date_str,
                description=description
            )
            created_type = 'research'
        else: # Institutional Duty
            entry = InstitutionalResponsibility.objects.create(
                user=user,
                academic_year=academic_year,
                responsibility_type='Administrative',
                position=title,
                description=description,
                from_date=date_str,
                to_date=date_str
            )
            created_type = 'institutional'

        return Response({'message': 'Activity created successfully', 'id': entry.id, 'type': created_type}, status=201)



