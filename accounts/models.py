from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, department, phone, password=None):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            full_name=full_name,
            department=department,
            phone=phone,
            is_staff=False,       # default value
            is_superuser=False    # default value
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, department, phone, password=None):
        user = self.create_user(
            email=email,
            full_name=full_name,
            department=department,
            phone=phone,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    DEPARTMENT_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Mathematics', 'Mathematics'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        ('English', 'English'),
        ('Commerce', 'Commerce'),
        ('Other', 'Other'),
    ]

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    phone = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)      # needed for admin
    is_superuser = models.BooleanField(default=False)  # needed for permissions

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'department', 'phone']

    def __str__(self):
        return self.email
