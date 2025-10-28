from django.db import models
from django.conf import settings
from django.utils import timezone
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


class Doctor(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100, blank=True)
    experience = models.PositiveIntegerField(default=0, help_text="Years of experience")
    clinic_name = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10)
    consultation_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Dr. {self.account.first_name} {self.account.last_name}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments'
    )
    doctor = models.ForeignKey(
        'Doctor', on_delete=models.CASCADE, related_name='appointments'
    )
    pet_name = models.CharField(max_length=100)
    reason = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.pet_name} - {self.user.first_name} with Dr. {self.doctor.account.first_name} on {self.date}"