from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms import RegisterForm
from django.urls import reverse_lazy

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:profile")
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"
