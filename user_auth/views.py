from rest_framework import viewsets,status,exceptions,permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate

from .tasks import send_email_verification_mail,send_password_reset_mail
from rest_framework.decorators import action
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .serializers import *
from .models import PasswordResets
import uuid
import datetime
import pytz

class UserAuthViewSet(viewsets.ViewSet):
    @action(detail = False,methods = ['POST'],url_path='token')
    def get_access_token(self,request):
        context = {
            'request':request
        }

        serializer = UserLoginSerializer(data = request.data,context=context)
        serializer.is_valid(raise_exception = True)

        return Response(serializer.validated_data)

    @action(detail = False,methods = ['POST'],url_path = 'token/refresh')
    def get_access_token_from_refresh_token(self,request):
        
        serializer = TokenRefreshSerializer(data = request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data,status = status.HTTP_200_OK)

            
    

    @action(detail = False,methods = ['GET'],url_path='verify-email')
    def verify_email(self,request):
        token = request.GET.get('token',None)
        email = request.GET.get('email',None)

        print(token,email)
        error_message = {
            'detail':'invalid verification link'
        }

        if token is None or email is None:
            raise exceptions.AuthenticationFailed(detail= error_message,code = status.HTTP_401_UNAUTHORIZED)

        user = None
        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            pass

        if user is None:    
            raise exceptions.AuthenticationFailed(detail=error_message,code = status.HTTP_401_UNAUTHORIZED)

        if str(user.verification_uuid) != token:
            raise exceptions.AuthenticationFailed(detail=error_message,code = status.HTTP_401_UNAUTHORIZED)

        user.is_verified = True
        user.save()

        response = {
            'message':'Email verified successfully'
        }
        return Response(response,status = status.HTTP_200_OK)

    @action(detail = False,methods = ['POST'])
    def register(self,request):
        serializer = UserRegistrationSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        user = User.objects.create_user(**serializer.validated_data)

        task = send_email_verification_mail.delay(user.id)
        
        response = {
            'message':'Verification link has been sent to '+user.email,
        }
        return Response(response)

    @action(detail = False,methods = ['GET'],url_path='password-reset',permission_classes=[permissions.IsAuthenticated])
    def password_reset(self,request):
    
        user = request.user

        print(type(user))

        _instance = PasswordResets.objects.create(user = user)

        response = {
            'message':'Follow the link sent to '+user.email,
        }

        send_password_reset_mail.delay(user.email,str(_instance.id),str(_instance.verification_token))
        
        return Response(response,status=status.HTTP_200_OK)

    @action(detail = False,methods = ['POST'],url_path='password-reset/confirm')
    def password_reset_confirm(self,request):
        uid = request.GET.get('uid',None)
        token = request.GET.get('token',None)
        user = request.user
        
        error_message = {
            'detail':'invalid verification link'
        }

        if token is None or uid is None:
            raise exceptions.AuthenticationFailed(detail= error_message,code = status.HTTP_401_UNAUTHORIZED)

        _instance = None

        try:
            _instance = PasswordResets.objects.get(pk = int(uid))
        except PasswordResets.DoesNotExist:
            raise exceptions.AuthenticationFailed(detail= error_message,code = status.HTTP_401_UNAUTHORIZED)

        if str(_instance.verification_token) != token:
            raise exceptions.AuthenticationFailed(detail= error_message,code = status.HTTP_401_UNAUTHORIZED)

        expiry = _instance.created + datetime.timedelta(minutes = 10)

        if pytz.utc.localize(datetime.datetime.utcnow()) > expiry:
            raise exceptions.AuthenticationFailed(detail= error_message,code = status.HTTP_401_UNAUTHORIZED)

        serializer = PasswordResetSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        if password != confirm_password:
            raise exceptions.ValidationError(detail='passwords do not match')

        user.set_password(password)
        user.save()

        response = {
            'message' : 'password changed successfully'
        }

        return Response(response,status = status.HTTP_200_OK)

    
    @action(detail = False,methods = ['POST'])
    def logout(self,request):
        pass



