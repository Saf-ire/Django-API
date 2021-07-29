''' User edit permission '''

#Django REST framework
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission

#Models
from django.contrib.auth.models import User
from users.models import Profile

class IsOwnProfile(BasePermission):
    ''' Check if the user trying to edit the profile is the owner '''

    def has_object_permission(self, request, view, obj):

        user_id = request.path.split('/')
        user_id = int(user_id[2])

        try:
            user = User.objects.get(username = request.user.username)
            if user.id == user_id:
                return True

        except user.DoesNotExist:
            return False
