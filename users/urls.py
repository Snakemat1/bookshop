from django.urls import path
from .views import RegisterView, ProfileView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name = "users/login.html", authentication_form=LoginForm), name="login"),
    path("logout/", LogoutView.as_view(next_page="catalog:book_list"), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile")
]
