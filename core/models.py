from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('worker', 'Worker'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class WorkerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    services = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='worker_services', null=True, blank=True)
    bio = models.TextField()
    experience = models.IntegerField()  # Add this field
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # Add this field

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_bookings')
    worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='worker_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Booking {self.id} - {self.user.username} to {self.worker.username}"

class Feedback(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()

    def __str__(self):
        return f"Feedback for Booking {self.booking.id} - Rating: {self.rating}"
