from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from meta.models import ModelMeta


class Inquiry(models.Model, ModelMeta):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    company_name = models.CharField(max_length=100)
    company_address = models.TextField()
    issue = models.TextField()
    message = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    _metadata = {
        'title': 'name',
        'description': 'message',
        'keywords': ['contact', 'inquiry', 'support'],
    }

    class Meta:
        verbose_name_plural = "Inquiries"
        ordering = ['-created_at']

    def get_absolute_url(self):
        # Return a valid URL, such as the homepage or a list of inquiries
        return reverse('contacts:inquiry_form')

    def __str__(self):
        return f"{self.name} - {self.subject}"


class NewsletterSubscription(models.Model, ModelMeta):
    given_name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, null=True, blank=True, default='')
    subscribed_at = models.DateTimeField(auto_now_add=True)

    _metadata = {
        'title': 'email',
        'description': 'Newsletter subscription',
        'keywords': ['newsletter', 'subscription', 'updates'],
    }

    class Meta:
        verbose_name_plural = "Newsletter Subscriptions"
        ordering = ['-subscribed_at']

    def __str__(self):
        return f"{self.given_name} {self.family_name} - {self.email}"
