from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import (
    SkillTag, Profile, JobListing, ApplicationOutcome,
    STATUS_CHOICES,
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

    user = User.objects.create_user(username=username, email=email, password=password)
    # Every user gets a Profile up front (lazily ensured elsewhere too).
    Profile.objects.get_or_create(user=user)
    return Response(_auth_payload(user), status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is None:
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
        if role_type:
            qs = qs.filter(role_type=role_type)
        if search:
            from django.db.models import Q
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
    job = get_object_or_404(JobListing, pk=request.data.get('job'))

    status_value = request.data.get('status')
    valid_statuses = {choice[0] for choice in STATUS_CHOICES}
    if status_value not in valid_statuses:
        return Response(
            {'detail': 'A valid outcome status is required.'}, status=400
        )

    defaults = {
        'status': status_value,
        'channel': request.data.get('channel', ''),
        'interview_format': request.data.get('interview_format', ''),
        'timeline': request.data.get('timeline', ''),
        'notes': request.data.get('notes', ''),
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
