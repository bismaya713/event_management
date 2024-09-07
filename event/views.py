from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Booking
from .forms import EventForm, BookingForm

# Admin View to Add Event
@login_required
def add_event(request):
    if not request.user.is_superuser:  # Only admins can add events
        return redirect('event:admin_event_list')

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, 'Event has been created successfully!')
            return redirect('event:admin_event_list')
    else:
        form = EventForm()
    
    return render(request, 'admin/add_event.html', {'form': form})

# Admin View to Edit Event
@login_required
def edit_event(request, event_id):
    if not request.user.is_superuser:  # Only admins can edit events
        return redirect('event:admin_event_list')

    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event has been updated successfully!')
            return redirect('event:admin_event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'admin/edit_event.html', {'form': form, 'event': event})

# Admin View to Delete Event
@login_required
def delete_event(request, event_id):
    if not request.user.is_superuser:  # Only admins can delete events
        return redirect('event:admin_event_list')

    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event has been deleted successfully!')
        return redirect('event:admin_event_list')

    return render(request, 'admin/delete_event.html', {'event': event})

@login_required
def admin_event_list(request):
    if not request.user.is_superuser:  # Only admins can see this view
        return redirect('event:event_list')

    events = Event.objects.all()
    return render(request, 'admin/event_list.html', {'events': events})
55679565280

@login_required
def admin_event_detail(request, event_id):
    if not request.user.is_superuser:  # Only admins can access this view
        return redirect('event:event_list')

    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'admin/event_details.html', {'event': event})


# User View to List Events
def user_event_list(request):
    events = Event.objects.all()
    return render(request, 'user/user_event_list.html', {'events': events})

def user_event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    form = BookingForm()  # Ensure form is included for booking

    context = {
        'event': event,
        'form': form
    }
    return render(request, 'user/user_event_list.html', context)


# User View to Book an Event
@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if booking.seats_booked > event.available_seats:
                messages.error(request, 'Not enough seats available.')
            else:
                event.available_seats -= booking.seats_booked
                event.save()
                booking.user = request.user
                booking.event = event
                booking.save()
                messages.success(request, 'Booking confirmed!')
                return redirect('event:event_list')
    else:
        form = BookingForm()

    return render(request, 'user/book_event.html', {'event': event, 'form': form})

# User View to See Event Details
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'user/user_event_detail.html', {'event': event})

# User View to See Bookings
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user/my_bookings.html', {'bookings': bookings})

