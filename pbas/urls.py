from django.urls import path
from .views import (
    TeachingEntryListCreateView, TeachingEntryDetailView, 
    StudentSupportListCreateView, StudentSupportDetailView,
    ResearchListCreateView, ResearchDetailView,
    AcademicContributionListCreateView, AcademicContributionDetailView,
    InstitutionalResponsibilityListCreateView, InstitutionalResponsibilityDetailView,
    PBASSummaryView,
    ScoringRuleListCreateView, ScoringRuleDetailView,
    AppraisalPeriodListCreateView, AppraisalPeriodDetailView,
    ActivityEvidenceListCreateView, ActivityEvidenceDetailView,
    NotificationListCreateView, NotificationDetailView,
    NotificationMarkReadView, NotificationMarkAllReadView
)

urlpatterns = [
    path('notifications/', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('notifications/<int:pk>/mark-read/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('notifications/mark-all-read/', NotificationMarkAllReadView.as_view(), name='notification-mark-all-read'),
    path('summary/', PBASSummaryView.as_view(), name='pbas-summary'),
    path('rules/', ScoringRuleListCreateView.as_view(), name='rules-list-create'),
    path('rules/<int:pk>/', ScoringRuleDetailView.as_view(), name='rules-detail'),
    path('appraisal-period/', AppraisalPeriodListCreateView.as_view(), name='appraisal-period-list-create'),
    path('appraisal-period/<int:pk>/', AppraisalPeriodDetailView.as_view(), name='appraisal-period-detail'),
    path('evidence/', ActivityEvidenceListCreateView.as_view(), name='evidence-list-create'),
    path('evidence/<int:pk>/', ActivityEvidenceDetailView.as_view(), name='evidence-detail'),
    path('teaching/', TeachingEntryListCreateView.as_view(), name='teaching-list-create'),
    path('teaching/<int:pk>/', TeachingEntryDetailView.as_view(), name='teaching-detail'),
    path('student-support/', StudentSupportListCreateView.as_view(), name='student-support-list-create'),
    path('student-support/<int:pk>/', StudentSupportDetailView.as_view(), name='student-support-detail'),
    path('research/', ResearchListCreateView.as_view(), name='research-list-create'),
    path('research/<int:pk>/', ResearchDetailView.as_view(), name='research-detail'),
    path('academic-contributions/', AcademicContributionListCreateView.as_view(), name='academic-contribution-list-create'),
    path('academic-contributions/<int:pk>/', AcademicContributionDetailView.as_view(), name='academic-contribution-detail'),
    path('institutional-responsibilities/', InstitutionalResponsibilityListCreateView.as_view(), name='institutional-responsibility-list-create'),
    path('institutional-responsibilities/<int:pk>/', InstitutionalResponsibilityDetailView.as_view(), name='institutional-responsibility-detail'),
]

