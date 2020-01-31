import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .models import Profile
from .serializers import ProfileSerializer
from django.http import HttpResponse
from django.conf import settings
from django.http import Http404



class Callback(APIView):
    def get(self,request):
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
            profile = Profile.objects.get(vk_id=user_id)
        except Profile.DoesNotExist:
            profile = Profile(vk_id=user_id,first_name=first_name, last_name=last_name,access_token=access_token)
            profile.save()

        return HttpResponseRedirect('/api/profiles/')

# class Profiles(APIView):
#     def get(self,request):
#         profiles = Profile.objects.all()
#         serializer = ProfileSerializer(profiles, many=True)
#         return Response(serializer.data)

# class Profile_Details(APIView):
#     def get(self,request, profile_id):
#         try:
#             profiles = Profile.objects.get(id=profile_id)
#             serializer = ProfileSerializer(profiles)
#             return Response(serializer.data)
#         except Profile.DoesNotExist:
#             raise Http404("")

class Profiles(ViewSet):
	
    def list(self, request):  #В листе уже встроен get или как это работает БЕЗ GET?
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def get(self, request, profile_id):
        try:
            profiles = Profile.objects.get(id=profile_id)
            serializer = ProfileSerializer(profiles)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            raise Http404("")