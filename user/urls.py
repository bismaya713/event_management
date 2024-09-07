from django.urls import path
from user import views
from django.conf import settings
from django.conf.urls.static import static
from user import forms
from django.contrib.auth import views as auth_view
app_name = 'user'


urlpatterns = [
    #Authentication urls
    path('', views.HomeView.as_view(), name='home'),
    path('admin/', views.AdminDashboard.as_view(), name='admin_dashboard'),
    path('register', views.Registration.as_view(), name = "register"),
    path('login', views.Login.as_view(), name = "login"),
    # path('forgot_password/', views.ForgotPasswordView.as_view(), name = "forgot_password"),
    path('reset-password/<uuid:token>/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('logout/', views.Logout.as_view(), name = "logout"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)