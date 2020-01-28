from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
    
    def create(self, validated_data):
        return Profile.objects.create(**validated_data)
        
    def update(self, instance, validated_data):
        instance.vk_id = validated_data.get('vk_id', instance.vk_id)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.access_token = validated_data.get('access_token', instance.access_token)
        instance.save()
