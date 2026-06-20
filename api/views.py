from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import (
    SkillTag, Profile, JobListing, ApplicationOutcome,
    STATUS_CHOICES, CHANNEL_CHOICES, INTERVIEW_FORMAT_CHOICES, ROLE_TYPE_CHOICES,
)
from .serializers import (
    SkillTagSerializer, ProfileSerializer, JobListSerializer,
    JobDetailSerializer, OutcomeSerializer, UserSerializer,
)
from .skill_gap import analyze_skill_gap


def _auth_payload(user):
    """Shape App.handleAuth expects: { token, user: { username, ... } }."""
    token, _ = Token.objects.get_or_create(user=user)
    return {'token': token.key, 'user': UserSerializer(user).data}


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = (request.data.get('username') or '').strip()
    email = (request.data.get('email') or '').strip()
    password = request.data.get('password') or ''

    if not username or not password:
        return Response(
            {'detail': 'Username and password are required.'}, status=400
        )
    if User.objects.filter(username__iexact=username).exists():
        return Response(
            {'detail': 'That username is already taken.'}, status=400
        )
    # Enforce Django's configured password policy (length/common/numeric checks).
    try:
        validate_password(password)
    except DjangoValidationError as exc:
        return Response({'detail': ' '.join(exc.messages)}, status=400)

    try:
        user = User.objects.create_user(username=username, email=email, password=password)
    except IntegrityError:
        # Defensive: covers a race between the existence check and create.
        return Response({'detail': 'That username is already taken.'}, status=400)
    # Every user gets a Profile up front (lazily ensured elsewhere too).
    Profile.objects.get_or_create(user=user)
    return Response(_auth_payload(user), status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = (request.data.get('username') or '').strip()
    password = request.data.get('password') or ''
    if not username or not password:
        return Response(
            {'detail': 'Username and password are required.'}, status=400
        )
    user = authenticate(username=username, password=password)
    if user is None:
        # Generic message on purpose — don't reveal whether the username exists.
        return Response({'detail': 'Invalid username or password.'}, status=400)
    return Response(_auth_payload(user))


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile


class JobListView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = JobListing.objects.all()
        role_type = self.request.query_params.get('role_type')
        search = self.request.query_params.get('search')
        # Unknown/malformed role_type values are ignored (treated as "no filter")
        # rather than erroring, so a stray query param never breaks the public
        # listing page. Only recognised role types narrow the results.
        valid_role_types = {value for value, _label in ROLE_TYPE_CHOICES}
        if role_type and role_type in valid_role_types:
            qs = qs.filter(role_type=role_type)
        if search:
            qs = qs.filter(Q(company__icontains=search) | Q(role__icontains=search))
        return qs


class JobDetailView(generics.RetrieveAPIView):
    queryset = JobListing.objects.all()
    serializer_class = JobDetailSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def skill_gap(request, pk):
    job = get_object_or_404(JobListing, pk=pk)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return Response(analyze_skill_gap(profile, job))


class OutcomeListView(generics.ListAPIView):
    serializer_class = OutcomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ApplicationOutcome.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_outcome(request):
    # Resolve the job safely: a missing id is a 400, an unknown/non-integer id
    # is a 404 — neither should ever surface as a 500.
    job_id = request.data.get('job')
    if job_id in (None, ''):
        return Response({'job': ['This field is required.']}, status=400)
    try:
        job = JobListing.objects.get(pk=job_id)
    except (JobListing.DoesNotExist, ValueError, TypeError):
        return Response(
            {'job': [f'No job listing found with id "{job_id}".']}, status=404
        )

    # Validate choice fields with clear, field-specific messages.
    errors = {}

    status_value = request.data.get('status')
    valid_statuses = {value for value, _label in STATUS_CHOICES}
    if status_value not in valid_statuses:
        errors['status'] = [
            'A valid outcome status is required: ' + ', '.join(sorted(valid_statuses)) + '.'
        ]

    channel = request.data.get('channel') or ''
    valid_channels = {value for value, _label in CHANNEL_CHOICES}
    if channel and channel not in valid_channels:
        errors['channel'] = [
            f'"{channel}" is not a valid channel. Choose one of: '
            + ', '.join(sorted(valid_channels)) + '.'
        ]

    interview_format = request.data.get('interview_format') or ''
    valid_formats = {value for value, _label in INTERVIEW_FORMAT_CHOICES}
    if interview_format and interview_format not in valid_formats:
        errors['interview_format'] = [
            f'"{interview_format}" is not a valid interview format. Choose one of: '
            + ', '.join(sorted(valid_formats)) + '.'
        ]

    if errors:
        return Response(errors, status=400)

    defaults = {
        'status': status_value,
        'channel': channel,
        'interview_format': interview_format,
        'timeline': request.data.get('timeline') or '',
        'notes': request.data.get('notes') or '',
    }
    # Upsert so re-submitting updates the existing outcome (unique per user+job).
    outcome, _ = ApplicationOutcome.objects.update_or_create(
        user=request.user, job=job, defaults=defaults
    )
    return Response(OutcomeSerializer(outcome).data)


class SkillListView(generics.ListAPIView):
    queryset = SkillTag.objects.all()
    serializer_class = SkillTagSerializer
    permission_classes = [AllowAny]
