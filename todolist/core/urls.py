from django.urls import path

from core import views

urlpatterns = [
    path('register/', views.UserCreateView.as_view()),
    path('profile/<int:pk>', views.UserDetailView.as_view()),
    path('update/<int:pk>', views.UserUpdateView.as_view()),
    path('delete/<int:pk>', views.UserDeleteView.as_view()),
    
]