from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse,reverse_lazy

# Create your models here.
class Clinics(models.Model):
    name=models.CharField(max_length=100,primary_key=True)
    address=models.TextField(max_length=200)
    city=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Doctors(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="doctor_profile")
    name=models.CharField(max_length=100)
    clinic_name=models.ManyToManyField("Clinics",related_name="resp_clinic")
    qualf=models.TextField(max_length=100,blank=False)
    special=models.TextField(max_length=100,blank=False)
    contact_no=models.CharField(max_length=10)
    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse('account:detail_doctor',kwargs={'username':self.user.username,'pk':self.pk})

class FixAppt(models.Model):
    fix_patient=models.ForeignKey("Patients",default="pat",on_delete=models.CASCADE,related_name="reg_patient")
    fix_doctor=models.ForeignKey("Doctors",default="doc",on_delete=models.CASCADE,related_name="selected_doctor")
    fix_clinic=models.ForeignKey("Clinics",default="clin",on_delete=models.CASCADE,related_name="selected_clinic")
    subject=models.TextField(max_length=100)


class Patients(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="patient_profile")
    name=models.CharField(max_length=100)
    age=models.PositiveSmallIntegerField()
    contact_no=models.CharField(max_length=10)
    email = models.EmailField(blank=True)
    def __str__(self):
        return self.user.username

