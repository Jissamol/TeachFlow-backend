from django.db import models
from accounts.models import User

class TeachingEntry(models.Model):
    LEVEL_CHOICES = [
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('Other', 'Other'),
    ]

    MODE_CHOICES = [
        ('Lecture', 'Lecture'),
        ('Practical', 'Practical'),
        ('Tutorial', 'Tutorial'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teaching_entries')
    academic_year = models.CharField(max_length=20)
    course_name = models.CharField(max_length=255)
    course_level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    mode_of_teaching = models.CharField(max_length=20, choices=MODE_CHOICES)
    classes_assigned = models.IntegerField()
    classes_taught = models.IntegerField()
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_name} ({self.academic_year})"


class StudentSupportEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_support_entries')
    academic_year = models.CharField(max_length=20)
    activity_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_audience = models.CharField(max_length=255)
    hours_spent = models.IntegerField()
    supporting_image = models.ImageField(upload_to='pbas/student_support/', blank=True, null=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity_name} ({self.academic_year})"


class ResearchEntry(models.Model):
    RESEARCH_TYPES = [
        ('Journal', 'Journal Publication'),
        ('Conference', 'Conference Paper'),
        ('Project', 'Research Project'),
        ('Guidance', 'Research Guidance (PhD/MPhil)'),
        ('Patent', 'Patent/Copyright'),
        ('Book', 'Book/Book Chapter'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='research_entries')
    academic_year = models.CharField(max_length=20)
    research_type = models.CharField(max_length=20, choices=RESEARCH_TYPES)
    title = models.CharField(max_length=500)
    journal_or_funding = models.CharField(max_length=500, help_text="Journal name or Funding agency")
    status_or_impact = models.CharField(max_length=100, help_text="Impact Factor, Status (Ongoing/Completed), etc.")
    supporting_image = models.ImageField(upload_to='pbas/research/', blank=True, null=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.research_type}: {self.title[:50]}..."


class AcademicContribution(models.Model):
    CONTRIBUTION_TYPES = [
        ('Invited Lecture', 'Invited Lecture'),
        ('Resource Person', 'Resource Person'),
        ('Paper Presentation', 'Paper Presentation'),
        ('Award/Fellowship', 'Award/Fellowship'),
        ('Policy Document', 'Policy Document'),
        ('Other', 'Other Academic Achievement'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='academic_contributions')
    academic_year = models.CharField(max_length=20)
    contribution_type = models.CharField(max_length=50, choices=CONTRIBUTION_TYPES)
    title = models.CharField(max_length=500)
    event_name = models.CharField(max_length=500)
    organization = models.CharField(max_length=500)
    date = models.DateField()
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    supporting_image = models.ImageField(upload_to='pbas/academic/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contribution_type}: {self.title[:50]}..."


class InstitutionalResponsibility(models.Model):
    RESP_TYPES = [
        ('Administrative', 'Administrative (IQAC/HOD/Dean)'),
        ('Committee', 'Committee Member/Coordinator'),
        ('Examination', 'Examination/Evaluation Duty'),
        ('Admission', 'Admission Related'),
        ('Student Welfare', 'Student Welfare/Co-curricular'),
        ('Other', 'Other Institutional Duty'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='institutional_responsibilities')
    academic_year = models.CharField(max_length=20)
    responsibility_type = models.CharField(max_length=50, choices=RESP_TYPES)
    position = models.CharField(max_length=255)
    description = models.TextField()
    supporting_image = models.ImageField(upload_to='pbas/institutional/', blank=True, null=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.responsibility_type}: {self.position}"
