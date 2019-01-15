from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator

class Facility(models.Model):
    def __str__(self):
        return self.F_Name

    F_Name = models.CharField(max_length=50, primary_key=True)
    F_Type = models.CharField(max_length=15, blank=True, null=True)
    Location = models.CharField(max_length=100)
    Description = models.TextField()
    Facility_Hours = models.TextField(blank=True, null=True)
    Facility_Phone = models.CharField(max_length=15, blank=True, null=True)
    Parking_Hours = models.TextField()


class Court(models.Model):
    def __str__(self):
        return self.C_Name

    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)

    C_Name = models.CharField(max_length=50, null=True)
    C_Type = models.CharField(max_length=50, null=True)
    current_count = models.IntegerField(default=0)


class Our_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    user_type = models.IntegerField(default=0)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Our_User.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.our_user.save()


class Reserved_Time_Slot(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    person = models.ForeignKey(Our_User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)


class Time_Slot(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE)

    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    available = models.BooleanField(default=True)
    signup_count = models.IntegerField(default=0, validators=[MinValueValidator(0)])
