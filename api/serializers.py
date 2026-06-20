from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    SkillTag, Profile, JobListing, ApplicationOutcome, Alumni,
    FACULTY_CHOICES, YEAR_CHOICES, GPA_CHOICES,
)


def _choice_values(choices):
    return ', '.join(value for value, _label in choices)


class SkillTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillTag
        fields = ['id', 'name', 'category']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    skills = SkillTagSerializer(many=True, read_only=True)
    # ProfilePage.jsx sends `skill_ids`; map it onto the `skills` M2M (write-only).
    # Custom messages name the offending id instead of DRF's generic "object does not exist".
    skill_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, required=False,
        queryset=SkillTag.objects.all(), source='skills',
        error_messages={
            'does_not_exist': 'Invalid skill id "{pk_value}" — no skill with that id exists.',
            'incorrect_type': 'Skill ids must be integers; got {data_type} instead.',
        },
    )
    # Explicit choice fields so a wrong value yields a clear, field-level message
    # (listing the accepted values) rather than DRF's terse default.
    faculty = serializers.ChoiceField(
        choices=FACULTY_CHOICES, required=False, allow_blank=True,
        error_messages={'invalid_choice':
                        'Invalid faculty. Choose one of: ' + _choice_values(FACULTY_CHOICES) + '.'},
    )
    year_of_study = serializers.ChoiceField(
        choices=YEAR_CHOICES, required=False, allow_blank=True,
        error_messages={'invalid_choice':
                        'Invalid year of study. Choose one of: ' + _choice_values(YEAR_CHOICES) + '.'},
    )
    gpa_range = serializers.ChoiceField(
        choices=GPA_CHOICES, required=False, allow_blank=True,
        error_messages={'invalid_choice':
                        'Invalid GPA range. Choose one of: ' + _choice_values(GPA_CHOICES) + '.'},
    )

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'faculty', 'major', 'year_of_study', 'gpa_range',
            'experiences', 'projects', 'portfolio_links', 'linkedin_url',
            'skills', 'skill_ids',
        ]


class AlumniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumni
        # email intentionally hidden from the public API
        fields = ['id', 'name', 'linkedin_url', 'company', 'current_role',
                  'graduation_year', 'faculty']


def _offer_outcomes(job):
    return job.outcomes.filter(status='offer').select_related('user__profile')


def _total_applications(job):
    return job.outcomes.count()


def _offer_rate(job):
    total = _total_applications(job)
    if not total:
        return 0
    offers = job.outcomes.filter(status='offer').count()
    return round(offers / total * 100)


class JobListSerializer(serializers.ModelSerializer):
    total_applications = serializers.SerializerMethodField()
    offer_rate = serializers.SerializerMethodField()

    class Meta:
        model = JobListing
        fields = ['id', 'company', 'role', 'role_type', 'deadline',
                  'total_applications', 'offer_rate']

    def get_total_applications(self, job):
        return _total_applications(job)

    def get_offer_rate(self, job):
        return _offer_rate(job)


class JobDetailSerializer(JobListSerializer):
    required_skills = SkillTagSerializer(many=True, read_only=True)
    avg_year_of_study = serializers.SerializerMethodField()
    gpa_distribution = serializers.SerializerMethodField()
    alumni = serializers.SerializerMethodField()

    class Meta(JobListSerializer.Meta):
        fields = JobListSerializer.Meta.fields + [
            'description', 'application_link', 'required_skills',
            'avg_year_of_study', 'gpa_distribution', 'alumni',
        ]

    def get_avg_year_of_study(self, job):
        years = []
        for outcome in _offer_outcomes(job):
            profile = getattr(outcome.user, 'profile', None)
            if profile and profile.year_of_study.isdigit():
                years.append(int(profile.year_of_study))
        if not years:
            return None
        avg = round(sum(years) / len(years), 1)
        return int(avg) if avg == int(avg) else avg

    def get_gpa_distribution(self, job):
        distribution = {}
        for outcome in _offer_outcomes(job):
            profile = getattr(outcome.user, 'profile', None)
            if profile and profile.gpa_range:
                distribution[profile.gpa_range] = distribution.get(profile.gpa_range, 0) + 1
        return distribution

    def get_alumni(self, job):
        alumni = Alumni.objects.filter(company__iexact=job.company)
        return AlumniSerializer(alumni, many=True).data


class OutcomeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    job = serializers.PrimaryKeyRelatedField(queryset=JobListing.objects.all())

    class Meta:
        model = ApplicationOutcome
        fields = ['id', 'user', 'job', 'status', 'channel',
                  'interview_format', 'timeline', 'notes', 'created_at']
        read_only_fields = ['created_at']
