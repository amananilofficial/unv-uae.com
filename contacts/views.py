from .forms import InquiryForm
from products.models import Product  # Correct import
from .models import NewsletterSubscription, Inquiry
import string
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import InquiryForm, NewsletterSubscriptionForm
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie


def contact(request):
    """
    View to render the contact page.
    """
    return render(request, 'contacts/contact.html')


@ensure_csrf_cookie
def inquiry_form(request):
    """
    View to handle the inquiry form submission.
    """
    print("Method:", request.method)  # Debug print
    if request.method == 'POST':
        print("POST data:", request.POST)  # Debug print
        form = InquiryForm(request.POST)
        if form.is_valid():
            try:
                inquiry = form.save()
                print("Form saved successfully:", inquiry)  # Debug print
                messages.success(
                    request, 'Your inquiry has been submitted successfully!')

                return redirect('contacts:inquiry_form')
            except Exception as e:
                print("Error saving form or sending email:",
                      str(e))  # Debug print
                messages.error(
                    request, 'An error occurred while submitting your inquiry.')
        else:
            print("Form errors:", form.errors)  # Debug print
            messages.error(request, 'Please correct the errors in your form.')
    else:
        form = InquiryForm()

    return render(request, 'contacts/form.html', {
        'form': form,
        'submit_url': request.path,
    })


@ensure_csrf_cookie
def newsletter_subscription(request):
    """
    View to handle the newsletter subscription form submission.
    """
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Thank you for subscribing to our newsletter!')
            return redirect('contacts:newsletter_subscription')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NewsletterSubscriptionForm()

    return render(request, 'contacts/newsletter.html', {'form': form})


def subscription_success(request):
    """
    View to display the success message after a successful newsletter subscription.
    """
    return render(request, 'contacts/newsletter.html')
