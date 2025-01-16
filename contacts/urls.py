from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('contacts/', views.contact, name='contacts'),
    path('inquiry/', views.inquiry_form, name='inquiry_form'),
    path('newsletter/', views.newsletter_subscription, name='newsletter_subscription'),
    path('newsletter/success/', views.subscription_success, name='subscription_success'),
]
