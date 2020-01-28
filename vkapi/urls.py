from django.urls import path
from . import views

urlpatterns = [
    path('callback/', views.callback, name='callback'),
    path('profiles/<int:profile_id>/', views._profiles, name='_profiles'),
    path('profiles/', views.profiles, name='profiles')
]
