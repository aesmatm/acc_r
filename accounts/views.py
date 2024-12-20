from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CustomPasswordChangeForm

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('admin:index')
    
    def form_valid(self, form):
        messages.success(self.request, 'تم تغيير كلمة المرور بنجاح')
        return super().form_valid(form)
