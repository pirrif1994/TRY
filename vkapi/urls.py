from django.urls import path
from . import views

urlpatterns = [
    path('callback/', views.callback, name='callback'),
    path('profiles/<int:profile_id>/', views.profiles_details, name='profiles_details'),
    path('profiles/', views.profiles, name='profiles')
]
