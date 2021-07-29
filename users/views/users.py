#Django-REST framework
from rest_framework import mixins, status, viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

#Permissions
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsOwnProfile
#from users.permissions import IsOwnProfile


#Models
from users.models import Profile
from django.contrib.auth.models import User
from rest_framework.serializers import Serializer

#Serializer
from users.serializers.users import UserSerializer, NewUserSerializer
from users.serializers.signup import UserSignupSerializer
from users.serializers.verification import AccountVerificationSerializer


class UserListView(ListAPIView):
    """ List of the users with pagination """
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

class ProfileDataViewSet(mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    ''' Add profile's data '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnProfile]

    


@api_view(['GET'])
def users_list(request):
    if request.method == "GET":
        users = User.objects.filter(is_staff=False)
        serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        data = NewUserSerializer(user).data
        return Response(data)

@api_view(['POST'])
def account_verification(request):
    """ Account verification API view """
    if request.method == 'POST':
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Account verified'}
        return Response(data, status=status.HTTP_200_OK)

