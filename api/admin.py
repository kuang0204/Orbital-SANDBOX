from django.contrib import admin

from .models import SkillTag, Profile, JobListing, ApplicationOutcome, Alumni


@admin.register(SkillTag)
class SkillTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'faculty', 'major', 'year_of_study', 'gpa_range')
    list_filter = ('faculty', 'year_of_study', 'gpa_range')
    search_fields = ('user__username', 'major')
    filter_horizontal = ('skills',)


@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('company', 'role', 'role_type', 'deadline')
    list_filter = ('role_type', 'company')
    search_fields = ('company', 'role')
    filter_horizontal = ('required_skills',)


@admin.register(ApplicationOutcome)
class ApplicationOutcomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'channel', 'created_at')
    list_filter = ('status', 'channel', 'interview_format')
    search_fields = ('user__username', 'job__company')


@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'current_role', 'graduation_year', 'faculty')
    list_filter = ('company', 'faculty')
    search_fields = ('name', 'company')
