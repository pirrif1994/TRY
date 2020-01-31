from django.urls import path
from .views import Callback, Profiles

urlpatterns = [
    path('callback/', Callback.as_view(), name='callback'),
    path('profiles/<int:profile_id>/', Profiles.as_view({'get': 'get'}), name='profiles_details'),
    path('profiles/', Profiles.as_view({'get': 'list'}), name='profiles')
]
