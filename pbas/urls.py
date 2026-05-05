from django.urls import path
from .views import (
    TeachingEntryListCreateView, TeachingEntryDetailView, 
    StudentSupportListCreateView, StudentSupportDetailView,
    ResearchListCreateView, ResearchDetailView,
    AcademicContributionListCreateView, AcademicContributionDetailView,
    InstitutionalResponsibilityListCreateView, InstitutionalResponsibilityDetailView
)

urlpatterns = [
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
