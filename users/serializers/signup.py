""" Signup a user serializer """

#Django
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import password_validation
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives

#Django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#Models
from users.models import Profile
from django.contrib.auth.models import User

#Utilities
import jwt 
from datetime import timedelta

class UserSignupSerializer(serializers.Serializer):
    """ Handle signup data validation and user/profile creation """
    
    username = serializers.CharField(min_length=4, max_length=150, allow_blank=False, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(max_length=150, allow_blank=False, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, max_length=128, allow_blank=False)
    password_confirmation = serializers.CharField(min_length=8, max_length=128, allow_blank=False)

    def validate(self, data):
        """ Password validation """
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise serializers.ValidationError({'Error':'Passwords do not match'})

        password_validation.validate_password(password)
        return data

    def create(self, data):
        """ Handle user and profile creation """
        data.pop('password_confirmation')

        user = User.objects.create_user(
            username = data['username'],
            password = data['password'],
            email = data['email'],
        )

        profile = Profile(
            user = user,
            is_verified = False
        )

        profile.save()

        self.send_confirmation_email(user)

        return user


    def send_confirmation_email(self, user):
        """ Send account verification link to given user """

        verification_token = self.gen_verification_token(user)
        subject = f'Welcome @{user.username}! Verify your account to start using the App'
        from_email = 'Application <noreply@app.com>'
        content = render_to_string(
            'emails/account_verification.html',
            {'token': verification_token, 'user': user}
        )
        msg = EmailMultiAlternatives(
            subject, content, from_email, [user.email]
        )
        msg.attach_alternative(content, 'text/html')
        msg.send()

    def gen_verification_token(self, user):
        """ Create a JWT token used by the user to verify his account """

        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'confirmation_email' 
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return token

