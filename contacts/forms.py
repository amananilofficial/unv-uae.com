import phonenumbers
from django import forms
from django.core.exceptions import ValidationError
from .models import Inquiry, NewsletterSubscription


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone_number', 'subject',
                  'company_name', 'company_address', 'issue', 'message']

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Remove any spaces or special characters
            phone = ''.join(filter(str.isdigit, str(phone)))
            # Add country code if not present (assuming UAE +971)
            if len(phone) == 10:  # If it's a 10-digit number
                phone = '+971' + phone[1:]  # Remove the leading 0 and add +971
            elif len(phone) == 9:  # If it's a 9-digit number
                phone = '+971' + phone
            elif not phone.startswith('+'):
                phone = '+' + phone
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
        return email


class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['given_name', 'family_name', 'email', 'phone', 'company', 'job_title']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove any spaces or special characters
            phone = ''.join(filter(str.isdigit, str(phone)))
            # Add country code if not present (assuming UAE +971)
            if len(phone) == 10:  # If it's a 10-digit number
                phone = '+971' + phone[1:]  # Remove the leading 0 and add +971
            elif len(phone) == 9:  # If it's a 9-digit number
                phone = '+971' + phone
            elif not phone.startswith('+'):
                phone = '+' + phone
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.strip().lower()
        return email
