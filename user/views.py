from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.contrib import messages
from django.contrib import auth
from user.forms import SignUpForm,LoginForm,ForgotPasswordForm,ResetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import logout,login,authenticate
from user import models
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.views.generic.edit import FormView
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from user import decorator
from event.models import Event

class HomeView(View):
    template = "user/index.html"
    def get(self, request):
        events = Event.objects.order_by('-event_date')[:3]
        return render(request, self.template, {'events': events})

@method_decorator(decorator.super_admin_only, name='dispatch')
class AdminDashboard(View):
    template = "user/admin_home.html"

    def get(self, request):
        return render(request, self.template)


class Registration(View):
    model = models.User
    template = 'user/registration.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            contact = form.cleaned_data.get('contact')
            full_name = form.cleaned_data.get('full_name')

            try:
                new_user = self.model(email=email, full_name=full_name, contact=contact)
                new_user.set_password(password)
                new_user.save()
                new_user_login = authenticate(request, username=email, password=password)
                if new_user_login is not None:
                    login(request, new_user_login)
                    
                    context = {
                        'full_name': full_name,
                        'email': email,
                    }

                    send_template_email(
                        subject='Registration Confirmation',
                        template_name='users/email/register_email.html',
                        context=context,
                        recipient_list=[email]
                    )
                    
                    messages.success(request, "Registration successful! You are now logged in.")
                    return redirect('user:home')
                else:
                    messages.error(request, "Authentication failed. Please try again.")
            except Exception as e:
                print(e)
                messages.error(request, 'Something went wrong while registering your account. Please try again later.')
        else:
            messages.error(request, 'Please correct the errors below.')

        return render(request, self.template, {'form': form})


class Login(View):
    model=models.User
    template = "user/login.html"

    def get(self, request):
        form = LoginForm()
        form2 = ForgotPasswordForm()
        return render(request, self.template, {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            try:
                user = models.User.objects.get(email=email)
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    if user.is_superuser:
                        return redirect('user:admin_dashboard')
                    else:
                        return redirect('user:home')
                else:
                    messages.error(request, "Incorrect password")
            except models.User.DoesNotExist:
                messages.error(request, "Invalid email")
        
        return render(request, self.template, {'form': form})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('user:home')
# class ForgotPasswordView(View):
#     template_name = 'forgot_password.html' 

#     def get(self, request):
#         form = forms.ForgotPasswordForm()
#         return render(request, self.template_name, {'form2': form2})

#     def post(self, request):
#         form = forms.ForgotPasswordForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             try:
#                 user = models.User.objects.get(email=email)
#                 user.send_reset_password_email()  # Ensure this method generates the correct reset URL with the token
#                 return HttpResponse("Password reset email sent successfully.")
#             except models.User.DoesNotExist:
#                 return HttpResponse("No user found with this email address.")
#             except Exception as e:
#                 return HttpResponse(f"An error occurred: {e}")
#         return render(request, self.template_name, {'form2': form2})

 


class ResetPasswordView(View):
    template_name = 'reset_password.html'

    def get(self, request, token):
        form = forms.ResetPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, token):
        form = forms.ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if new_password != confirm_password:
                return HttpResponse("Passwords do not match.")
            try:
                user = models.User.objects.get(token=token)
                if user:
                    user.set_password(new_password)
                    user.token = None  # Clear the token after password reset
                    user.save()
                    messages.success(request, "Password reset successfully.")
                    return redirect('users:login')
                else:
                    return HttpResponse("Invalid token.")
            except models.User.DoesNotExist:
                return HttpResponse("Invalid token.")
        return render(request, self.template_name, {'form': form})


