from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('profile/', views.ProfileView.as_view()),
    path('jobs/', views.JobListView.as_view()),
    path('jobs/<int:pk>/', views.JobDetailView.as_view()),
    path('jobs/<int:pk>/skill-gap/', views.skill_gap),
    path('outcomes/', views.OutcomeListView.as_view()),
    path('outcomes/submit/', views.submit_outcome),
    path('skills/', views.SkillListView.as_view()),
]
