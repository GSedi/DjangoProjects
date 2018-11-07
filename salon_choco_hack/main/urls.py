from django.urls import path
from main import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('services/', views.ServiceList.as_view(), name='services_list'),
    path('services/<int:pk>/', views.ServiceDetail.as_view(), name='service_detail'),
    path('salons/', views.SalonList.as_view(), name='salon_list'),
    path('salons/<int:pk>/', views.SalonDetail.as_view(), name='salon_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
