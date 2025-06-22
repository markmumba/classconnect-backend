from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class School(models.Model):

    name = models.CharField(max_length=255,unique=True)
    email_domain= models.CharField(max_length=100,unique=True)
    location = models.TextField(max_length=100,blank=False)
    phone = models.CharField(max_length=100,blank=False)
    logo = models.ImageField(upload_to="school_logo/",blank=True,null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        db_table='school'
        ordering =['name']
    
    def __str__(self):
        return self.name
    

    @property
    def full_email_domain(self):
        return f"@{self.email_domain}"
    
    def clean(self):
        if self.email_domain:
            self.email_domain = self.email_domain.lstrip('@')
        
        if not '.'in self.email_domain:
            raise ValidationError({'email_domain':'Enter a valid domain(eg. university.edu)'})
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


    

class SubSchool(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE,related_name='departments')
    name = models.CharField(max_length=255)
    description=models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table='sub_schools'
        unique_together =['school','name']
        ordering =['school','name']


    def __str__(self):
        return f"{self.school.name} - {self.name}"