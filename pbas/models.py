from django.db import models
from accounts.models import User

class ScoringRule(models.Model):
    category = models.CharField(max_length=50)
    activity_type = models.CharField(max_length=100, unique=True)
    points_per_unit = models.FloatField(default=10.0)
    is_per_hour = models.BooleanField(default=False)
    max_capped_points = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.activity_type} ({self.points_per_unit} pts)"


def get_rule_score(activity_type, default_points, multiplier=1.0):
    try:
        rule = ScoringRule.objects.get(activity_type=activity_type)
        pts = rule.points_per_unit * (multiplier if rule.is_per_hour else 1.0)
        if rule.max_capped_points:
            pts = min(pts, rule.max_capped_points)
        return round(pts, 2)
    except ScoringRule.DoesNotExist:
        return round(default_points * multiplier, 2)


class AppraisalPeriod(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Under Review', 'Under Review'),
        ('Submitted', 'Submitted'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appraisal_periods')
    academic_year = models.CharField(max_length=20)
    title = models.CharField(max_length=255, default="Annual Appraisal")
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    target_score = models.FloatField(default=300.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'academic_year')

    def __str__(self):
        return f"{self.user.email} - {self.academic_year} ({self.status})"


class ActivityEvidence(models.Model):
    EVIDENCE_TYPES = [
        ('Certificate', 'Certificate'),
        ('Publication', 'Publication (PDF)'),
        ('Appointment Letter', 'Appointment Letter'),
        ('Attendance/Log', 'Attendance / Logbook'),
        ('Other', 'Other Evidence'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evidences')
    academic_year = models.CharField(max_length=20)
    category = models.CharField(max_length=50)
    activity_id = models.IntegerField(null=True, blank=True)
    activity_title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pbas/evidence/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50, choices=EVIDENCE_TYPES, default='Certificate')
    status = models.CharField(max_length=20, default='Verified')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} ({self.file_type})"


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
            return get_rule_score('Teaching Hour', 25.0, multiplier=percentage)
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
            return get_rule_score('Workshop', 2.0, multiplier=float(self.hours_spent) / 5.0)
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
        type_mapping = {
            'Journal': 'Journal Publication',
            'Conference': 'Conference Paper',
            'Guidance': 'PhD Guidance',
            'Project': 'Research Project',
            'Patent': 'Patent/Copyright',
            'Book': 'Book Chapter',
        }
        type_name = type_mapping.get(self.research_type, self.research_type)
        default_pts = 10.0
        if self.research_type == 'Journal': default_pts = 10.0
        elif self.research_type == 'Conference': default_pts = 5.0
        elif self.research_type == 'Guidance': default_pts = 15.0
        return get_rule_score(type_name, default_pts)

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
        return get_rule_score(self.contribution_type, 3.0)

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
        return get_rule_score(self.responsibility_type, 5.0)

    def save(self, *args, **kwargs):
        self.score = self.calculate_score()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.responsibility_type}: {self.position}"
