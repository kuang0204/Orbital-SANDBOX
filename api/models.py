from django.db import models
from django.contrib.auth.models import User


FACULTY_CHOICES = [
    ('SOC', 'School of Computing'),
    ('ENG', 'Faculty of Engineering'),
    ('BIZ', 'NUS Business School'),
    ('FASS', 'Faculty of Arts and Social Sciences'),
    ('SCI', 'Faculty of Science'),
    ('MED', 'Yong Loo Lin School of Medicine'),
    ('LAW', 'Faculty of Law'),
]

YEAR_CHOICES = [(str(y), f'Year {y}') for y in range(1, 7)]

GPA_CHOICES = [
    ('0.0-2.0', '0.0-2.0'),
    ('2.0-3.0', '2.0-3.0'),
    ('3.0-3.5', '3.0-3.5'),
    ('3.5-4.0', '3.5-4.0'),
    ('4.0-5.0', '4.0-5.0'),
]

ROLE_TYPE_CHOICES = [
    ('SWE', 'Software Engineering'),
    ('DS', 'Data Science'),
    ('PM', 'Product Management'),
    ('UIUX', 'UI/UX Design'),
    ('DE', 'Data Engineering'),
    ('ML', 'Machine Learning'),
    ('FS', 'Full Stack'),
    ('IT', 'Information Technology'),
    ('BA', 'Business Analysis'),
    ('OT', 'Other'),
]

STATUS_CHOICES = [
    ('offer', 'Offer'),
    ('rejection', 'Rejection'),
    ('pending', 'Pending'),
]

CHANNEL_CHOICES = [
    ('portal', 'Company Portal'),
    ('linkedin', 'LinkedIn'),
    ('careerfair', 'Career Fair'),
    ('referral', 'Referral'),
    ('email', 'Direct Email'),
    ('other', 'Other'),
]

INTERVIEW_FORMAT_CHOICES = [
    ('online', 'Online'),
    ('inperson', 'In-Person'),
    ('both', 'Both'),
    ('none', 'No Interview'),
]


class SkillTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    faculty = models.CharField(max_length=10, choices=FACULTY_CHOICES, blank=True)
    major = models.CharField(max_length=120, blank=True)
    year_of_study = models.CharField(max_length=2, choices=YEAR_CHOICES, blank=True)
    gpa_range = models.CharField(max_length=10, choices=GPA_CHOICES, blank=True)
    experiences = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    portfolio_links = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    skills = models.ManyToManyField(SkillTag, blank=True, related_name='profiles')

    def __str__(self):
        return f"Profile<{self.user.username}>"


class JobListing(models.Model):
    company = models.CharField(max_length=120)
    role = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    application_link = models.URLField(blank=True)
    deadline = models.DateField(null=True, blank=True)
    role_type = models.CharField(max_length=8, choices=ROLE_TYPE_CHOICES, default='OT')
    required_skills = models.ManyToManyField(SkillTag, blank=True, related_name='jobs')

    class Meta:
        # Insertion order — seed.py attaches outcomes by positional index
        # (jobs[0], jobs[2]), so this must stay stable and ascending.
        ordering = ['id']

    def __str__(self):
        return f"{self.company} — {self.role}"


class ApplicationOutcome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outcomes')
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, related_name='outcomes')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    channel = models.CharField(max_length=12, choices=CHANNEL_CHOICES, blank=True)
    interview_format = models.CharField(
        max_length=12, choices=INTERVIEW_FORMAT_CHOICES, blank=True
    )
    timeline = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} @ {self.job.company} ({self.status})"


class Alumni(models.Model):
    name = models.CharField(max_length=120)
    linkedin_url = models.URLField()
    email = models.EmailField(blank=True)
    company = models.CharField(max_length=120)
    current_role = models.CharField(max_length=160, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    faculty = models.CharField(max_length=10, choices=FACULTY_CHOICES, blank=True)

    class Meta:
        verbose_name_plural = 'Alumni'
        ordering = ['company', 'name']

    def __str__(self):
        return f"{self.name} ({self.company})"
