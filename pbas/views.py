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
