import csv
import io
import pandas as pd
from django.http import HttpResponse
from .models import Inquiry, NewsletterSubscription


def export_inquiries_to_csv(queryset):
    """
    Export the given queryset of Inquiries to a CSV file.
    """
    # Prepare CSV export for inquiries
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Email', 'Phone', 'Subject', 'Created At'])

    # Use iterator to prevent memory overload on large datasets
    for inquiry in queryset.iterator():
        writer.writerow([inquiry.name, inquiry.email,
                        inquiry.phone_number, inquiry.subject, inquiry.created_at])

    # Return the CSV content as a string
    return output.getvalue()


def export_inquiries_to_excel(queryset):
    """
    Export the given queryset of Inquiries to an Excel file.
    Uses pandas for Excel formatting.
    """
    data = []
    # Use iterator to prevent memory overload on large datasets
    for inquiry in queryset.iterator():
        data.append([inquiry.name, inquiry.email,
                    inquiry.phone_number, inquiry.subject, inquiry.created_at])

    # Create a DataFrame using pandas
    df = pd.DataFrame(
        data, columns=['Name', 'Email', 'Phone', 'Subject', 'Created At'])

    # Output the Excel file to a BytesIO object
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Inquiries')

    # Move the cursor to the beginning of the BytesIO object and return the data
    output.seek(0)
    return output.read()


def export_newsletters_to_csv(queryset):
    """
    Export the given queryset of NewsletterSubscriptions to a CSV file.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Given Name', 'Family Name', 'Email',
                    'Company', 'Date Subscribed'])

    # Use iterator to prevent memory overload on large datasets
    for subscription in queryset.iterator():
        writer.writerow([subscription.given_name, subscription.family_name,
                        subscription.email, subscription.company, subscription.date_subscribed])

    # Return the CSV content as a string
    return output.getvalue()


def export_newsletters_to_excel(queryset):
    """
    Export the given queryset of NewsletterSubscriptions to an Excel file.
    Uses pandas for Excel formatting.
    """
    data = []
    # Use iterator to prevent memory overload on large datasets
    for subscription in queryset.iterator():
        data.append([subscription.given_name, subscription.family_name,
                    subscription.email, subscription.company, subscription.date_subscribed])

    # Create a DataFrame using pandas
    df = pd.DataFrame(data, columns=[
                      'Given Name', 'Family Name', 'Email', 'Company', 'Date Subscribed'])

    # Loop through each column and convert datetime columns to timezone-naive
    for column in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            # Remove timezone information from datetime columns
            df[column] = df[column].dt.tz_localize(None)

    # Output the Excel file to a BytesIO object
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Newsletter Subscriptions')

    # Move the cursor to the beginning of the BytesIO object and return the data
    output.seek(0)
    return output.read()
