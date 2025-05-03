from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, WorkerProfile, Booking, Feedback, Service, Location

class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

class WorkerProfileForm(forms.ModelForm):
    class Meta:
        model = WorkerProfile
        fields = ['services', 'location', 'experience', 'bio']  

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []  # No additional fields are needed from user during booking, if applicable

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['review', 'rating']  # Corrected 'comments' to 'review'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name','location']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']
