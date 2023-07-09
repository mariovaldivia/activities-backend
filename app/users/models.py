"""User model."""
import os
# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify

# Utilities
from main.utils.models import BaseModel

def directory_user_path(instance, filename):
    """ Directory to store user's images """
    path = 'users/'
    name, extension = os.path.splitext(filename)
    return f"{path}{slugify(str(instance))}{extension}"


class Management(BaseModel):
    """ Management model """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Managements"
        ordering = ['-created']

class Department(BaseModel):
    """ Department model """
    name = models.CharField(max_length=50)
    management = models.ForeignKey(
        Management, 
        null=False, 
        on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.management}"

    class Meta:
        verbose_name_plural = "Departments"
        ordering = ['-created']

class User(BaseModel, AbstractUser):
    """User model.
    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17, blank=True)

    department = models.ForeignKey(
        Department, 
        null=True, 
        on_delete=models.SET_NULL)
    
    image = models.FileField(
        verbose_name='Imagen', 
        null=True,
        upload_to=directory_user_path,
        blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username
