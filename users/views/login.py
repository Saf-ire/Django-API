""" User login view """

#Django REST framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

#Serializers
from users.serializers.login import UserLoginSerializer
from users.serializers.users import UserSerializer

class UserLoginAPIView(APIView):
    """ User login api view """

    def post(self, request, *args, **kwargs):
        """ Handle HTTP POST request """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        
        data = {
            'user': UserSerializer(user).data,
            'token': token
        }

        return Response(data, status=status.HTTP_202_ACCEPTED)
