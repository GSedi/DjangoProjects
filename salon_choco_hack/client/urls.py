from django.urls import path
from client import views

urlpatterns = [
    path('clients/', views.ClientList.as_view(), name='clients_list'),
    path('clients/<int:pk>/', views.ClientDetail.as_view(), name='clients_detail'),
    path('auth/register/', views.register, name='client_register'),
    path('auth/login/', views.login, name='client_login'),
    path('auth/logout/', views.logout, name='client_logout'),
]
