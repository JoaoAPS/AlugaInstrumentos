from django.urls import path

from users import views


urlpatterns = [
    path('login/', views.AuthTokenView.as_view(), name='auth-token'),
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
]
