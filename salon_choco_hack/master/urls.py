from django.urls import path
from master import views

urlpatterns = [
    path('masters/', views.MasterList.as_view(), name='masters_list'),
    path('masters/<int:pk>/', views.MasterDetail.as_view(), name='masters_detail'),
    path('auth/register/', views.register, name='master_register'),
    path('auth/login/', views.login, name='master_login'),
    path('auth/logout/', views.logout, name='master_logout'),
]
