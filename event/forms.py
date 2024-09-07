from django import forms
from .models import Event, Booking

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['img','title', 'description', 'event_date', 'location', 'available_seats']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        img = forms.ImageField(label='image', required=True)
        img.widget.attrs.update({'class': 'form-control','type':'file'})

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seats_booked']
