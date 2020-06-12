from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password,first_name,last_name, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        """
        Dictionary.setdefault() returns the value of a key (if the key is in dictionary).
        If not, it inserts key with a value to the dictionary.
        
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,first_name = first_name,last_name = last_name, **extra_fields)
        user.set_password(password)
        """
        set_password hashes the password before saving it

        """
        user.save()
        return user

    def create_superuser(self, email, password,first_name,last_name, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password,first_name,last_name, **extra_fields)