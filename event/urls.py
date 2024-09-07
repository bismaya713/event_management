from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'event'


urlpatterns = [
    path('admin/events/', views.admin_event_list, name='admin_event_list'),
    path('admin/events/<int:event_id>/', views.admin_event_detail, name='admin_event_detail'),
    path('admin/add/', views.add_event, name='add_event'),
    path('admin/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('admin/delete/<int:event_id>/', views.delete_event, name='delete_event'),

    # User URLs
    path('user/event/', views.user_event_list, name='event_list'),
    path('<int:event_id>/', views.user_event_detail, name='event_detail'),
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
