from django.db import models
from user.models import User

class Event(models.Model):
    img= models.ImageField(upload_to="pic", blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    available_seats = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    seats_booked = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.seats_booked} seat(s) for {self.event.title}"
