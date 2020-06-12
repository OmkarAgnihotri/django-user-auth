from rest_framework import serializers,exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model,authenticate
from .models import PasswordResets



User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def get_token(self,user):
        return RefreshToken.for_user(user)
    
    def validate(self,attrs):
        authentication_kwargs = {
            'email':attrs['email'],
            'password':attrs['password']
        }

        request = self.context.get('request',None)

        user = authenticate(request,**authentication_kwargs)

        if user is None or not user.is_active or not user.is_verified:
            raise exceptions.AuthenticationFailed(detail = 'no active account with provided credentials')    

        data = {}

        refresh = self.get_token(user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password','first_name','last_name']

        extra_kwargs = {

            'password':{'write_only':True}
        }

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length = 128)
    confirm_password = serializers.CharField(max_length = 128)

   