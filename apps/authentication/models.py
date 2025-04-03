from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    CHOICE_ROLE = {
        'admin': 'Admin',
        'moderator': 'Moderator',
        'common_user': 'Common_user'
    }

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=CHOICE_ROLE, default='common_user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        return self.role == 'admin'
    
    @property
    def is_superuser(self):
        return self.role == 'admin'
    
    def has_perm(self, perm, obj=None):
        return self.role == 'admin'
    
    def has_module_perms(self, app_label):
        return self.role == 'admin'