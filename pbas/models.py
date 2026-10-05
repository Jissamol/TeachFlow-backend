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
    supporting_image = models.ImageField(upload_to='pbas/teaching/', blank=True, null=True)
    score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_score(self):
        if self.classes_assigned and self.classes_assigned > 0:
            percentage = min(1.0, float(self.classes_taught) / float(self.classes_assigned))
            return round(percentage * 25.0, 2)
        return 0.0

    def save(self, *args, **kwargs):
        self.score = self.calculate_score()
        super().save(*args, **kwargs)

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
    score = models.FloatField(default=0.0)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_score(self):
        if self.hours_spent:
            return min(15.0, round(float(self.hours_spent) / 5.0, 2))
        return 0.0

    def save(self, *args, **kwargs):
        self.score = self.calculate_score()
        super().save(*args, **kwargs)

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
    score = models.FloatField(default=0.0)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_score(self):
        weights = {
            'Journal': 25.0,
            'Conference': 10.0,
            'Project': 20.0,
            'Guidance': 15.0,
            'Patent': 30.0,
            'Book': 20.0,
        }
        return weights.get(self.research_type, 10.0)

    def save(self, *args, **kwargs):
        self.score = self.calculate_score()
        super().save(*args, **kwargs)

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
    score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_score(self):
        weights = {
            'Invited Lecture': 5.0,
            'Resource Person': 5.0,
            'Paper Presentation': 5.0,
            'Award/Fellowship': 10.0,
            'Policy Document': 10.0,
            'Other': 3.0,
        }
        return weights.get(self.contribution_type, 3.0)

    def save(self, *args, **kwargs):
        self.score = self.calculate_score()
        super().save(*args, **kwargs)

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
    score = models.FloatField(default=0.0)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_score(self):
        weights = {
            'Administrative': 10.0,
            'Committee': 5.0,
            'Examination': 5.0,
            'Admission': 5.0,
            'Student Welfare': 5.0,
            'Other': 3.0,
        }
        return weights.get(self.responsibility_type, 3.0)

    def save(self, *args, **kwargs):
        self.score = self.calculate_score()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.responsibility_type}: {self.position}"
