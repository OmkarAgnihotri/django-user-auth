# django-user-auth
Comprehensive user authentication using email verification  
# Usage guide
install following packages in the virtual environment  
1. django-rest-framework  
2. django-rest-framework-simplejwt  
3. celery  
  
Add the following to INSTALLED_APPS of django settings.py file  
1. user_auth  
2. rest_framework  
  
Add user_auth folder in your django project  

Follow celery documentation for setting up async tasks  

Run migrations  

# API endpoints

POST auth/token                     get access and refresh token providing user email and password  
POST auth/token/refresh             get access token from refresh token
POST auth/register                  create new user account--email verification mail will sent on the provided email  
GET auth/verify-email               verify provided email  
GET auth/password-reset             change password-email will be sent inorder to change current password
POST auth/password-reset/confirm    provide new password   
