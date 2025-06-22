from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from schools.models import School, SubSchool


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email)

        if 'school' not in extra_fields:
            domain = email.split('@')[1] if '@' in email else None
            if domain:
                try :
                    school = School.objects.get(email_domain=domain,is_active=True)
                    extra_fields['school'] = school
                except School.DoesNotExist:
                    raise ValueError(f'No active school found for domain: {domain}')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    quote = models.CharField(max_length=255,blank=True)
    picture = models.ImageField(upload_to="user_pictures/")
    career_path = models.CharField(max_length=100)

    school = models.ForeignKey(School, on_delete=models.CASCADE,related_name='users')
    sub_school = models.ForeignKey(SubSchool, on_delete=models.CASCADE,related_name='users')


    ROLE_CHOICES= [
        ('student','student'),
        ('teacher','teacher'),
        ('admin','School Admin'),
        ('super_admin','Super Admin')
    ]

    role = models.CharField(max_length=20 ,choices=ROLE_CHOICES,default='student')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table='users'
        indexes = [
            models.Index(fields=['school','email']),
            models.Index(fields=['school','role']),
        ]

    def __str__(self):
        return self.email
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def short_name(self):
        return self.first_name

    
    @property
    def is_school_admin(self):
        return self.role in ['admin','super_admin']

    def clean(self):
        if self.email and self.school:
            email_domain = self.email.split('@')[1] if '@' in self.email else None
            if email_domain != self.school.email_domain:
                raise ValidationError ({
                    'email':f'Email must belong to {self.school.email_domain} domain'
                })

    def save(self,*args,**kwargs):
        self.clean()
        super().save(*args,**kwargs)