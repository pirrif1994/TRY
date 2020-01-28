import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .models import Profile
from .serializers import ProfileSerializer
from django.http import HttpResponse
from django.conf import settings

@api_view(['GET'])
def callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({})
    url = f'https://oauth.vk.com/access_token?client_id={settings.VK_CLIENT_ID}&client_secret={settings.VK_SECRET}&redirect_uri=http://localhost:8000/api/callback/&code={code}'
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
    return HttpResponseRedirect('/api/profiles/')


@api_view(['GET'])
def profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def profiles_details(request, profile_id):
    try:
        profiles = Profile.objects.get(id=profile_id)
        serializer = ProfileSerializer(profiles)
        return Response(serializer.data)
    except Profile.DoesNotExist:
        return JsonResponse({"Detail":"Profile Does Not Exist", "status":"404"})
    