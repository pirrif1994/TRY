import requests
import io
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from .models import Profile
from .profile_serializer import ProfileSerializer
from django.http import HttpResponse

@api_view(['GET'])
def callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({})
    url = 'https://oauth.vk.com/access_token?client_id=7297032&client_secret=kPY7OUtPFEf8rqIGeFo3&redirect_uri=http://localhost:8000/api/callback/&code=' + code
    auth_info = requests.post(url).json()
    access_token = auth_info['access_token']
    user_id = auth_info['user_id']
    url = 'https://api.vk.com/method/users.get?user_ids=' + str(user_id) +'&access_token=' + access_token + "&v=5.103"
    profile_info = requests.post(url).json()
    first_name = profile_info['response'][0]['first_name']
    last_name = profile_info['response'][0]['last_name']
    try:
        profile = Profile.objects.get(vk_id=user_id,first_name=first_name, last_name=last_name)
    except Profile.DoesNotExist:
        profile = Profile(vk_id=user_id,first_name=first_name, last_name=last_name,access_token=access_token)
        profile.save()
    serializer = ProfileSerializer(profile)
    serializer = ProfileSerializer(profile)
    posts = Profile.objects.all()
    return HttpResponseRedirect('/?done')


@api_view(['GET'])
def profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def _profiles(request, profile_id):
    try:
        profiles = Profile.objects.get(id=profile_id)
        serializer = ProfileSerializer(profiles)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        return HttpResponse("<h1>Error: Wrong id<h1>")
    