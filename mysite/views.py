from django.shortcuts import render
from vkapi.models import Profile


def post_list(request):
    posts = Profile.objects.all()
    return render(request, 'vkapi/post_list.html', {'posts':posts})