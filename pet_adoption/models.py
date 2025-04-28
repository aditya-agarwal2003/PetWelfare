from django.db import models
from accounts.models import Account
from cloudinary.models import CloudinaryField

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(Account, on_delete=models.RESTRICT)
    name = models.CharField(max_length=25)
    image = CloudinaryField('image')
    description = models.TextField(max_length=500,blank=True)
    post_address = models.CharField(max_length=100,blank=True)
    price = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    DOG = 'dog'
    CAT = 'cat'
    BIRD = 'bird'
    MISC = 'misc.'
    CATEGORY_CHOICES = (
        (DOG, DOG),
        (CAT, CAT),
        (BIRD, BIRD),
        (MISC, MISC),
    )

    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'
    GENDER_CHOICES = (
        (MALE, MALE),
        (FEMALE, FEMALE),
        (UNKNOWN, UNKNOWN),
    )
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now=True)


class AdoptionRequest(models.Model):
    user = models.ForeignKey(Account, on_delete=models.RESTRICT)
    post = models.ForeignKey(Post, on_delete=models.RESTRICT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now=True)


class Contact(models.Model):
    name = models.CharField(max_length=35)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=500,blank=True)
