from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('internship/', views.internship, name='internship'),
    path('internship/apply/', views.internship_apply, name='internship_apply'),
    path('contact/', views.contact, name='contact'),

    path('api/contact/', views.contact_api, name='contact_api'),

    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms, name='terms'),
]