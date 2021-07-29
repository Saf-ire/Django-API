""" User Serializers """

#Django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#Models
from django.contrib.auth.models import User
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """ Profile model serializer """

    class Meta:
        model = Profile
        fields = ['title', 'rank', 'level', 'profile_picture', 'header_img']

class UserSerializer(serializers.ModelSerializer):
    """ User serializer """

    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']

    def update(self, instance, validated_data):
    
        profile_data = validated_data.pop('profile')

        profile = instance.profile
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        
        instance.save()

        profile.title = profile_data.get('title', profile.title)
        profile.rank = profile_data.get('rank', profile.rank)
        profile.level = profile_data.get('level', profile.level)
        profile.profile_picture = profile_data.get('profile_picture', profile.profile_picture)
        profile.header_img = profile_data.get('header_img', profile.header_img)
    
        profile.save()
        
        return instance

class NewUserSerializer(serializers.ModelSerializer): 
    ''' Return data for a new user '''

    class Meta:
        model = User
        fields = ['username']
