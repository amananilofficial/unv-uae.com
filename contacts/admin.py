from django.contrib import admin
from django.http import HttpResponse
from .models import Inquiry, NewsletterSubscription
from .utils import export_inquiries_to_csv, export_inquiries_to_excel, export_newsletters_to_csv, export_newsletters_to_excel
from import_export.admin import ImportExportModelAdmin


@admin.register(Inquiry)
class InquiryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'subject', 'created_at')
    list_filter = ('created_at', 'subject')
    search_fields = ('name', 'email', 'phone_number',
                     'subject', 'company_name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('name', 'email', 'phone_number', 'message',
                                           'subject', 'company_name', 'company_address', 'issue')
        return self.readonly_fields

    actions = ['export_inquiries_to_csv_action',
               'export_inquiries_to_excel_action']

    def export_inquiries_to_csv_action(self, request, queryset):
        csv_data = export_inquiries_to_csv(queryset)
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inquiries.csv"'
        return response

    def export_inquiries_to_excel_action(self, request, queryset):
        excel_file = export_inquiries_to_excel(queryset)
        response = HttpResponse(
            excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="inquiries.xlsx"'
        return response

    export_inquiries_to_csv_action.short_description = "Export selected inquiries to CSV"
    export_inquiries_to_excel_action.short_description = "Export selected inquiries to Excel"


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(ImportExportModelAdmin):
    list_display = ('given_name', 'family_name',
                    'email', 'company', 'subscribed_at')
    list_filter = ('company', 'subscribed_at')
    search_fields = ('given_name', 'family_name', 'email', 'company')
    readonly_fields = ('subscribed_at',)
    date_hierarchy = 'subscribed_at'
    actions = ['export_newsletters_to_csv_action',
               'export_newsletters_to_excel_action']

    def export_newsletters_to_csv_action(self, request, queryset):
        csv_data = export_newsletters_to_csv(queryset)
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="newsletter_subscriptions.csv"'
        return response

    def export_newsletters_to_excel_action(self, request, queryset):
        excel_file = export_newsletters_to_excel(queryset)
        response = HttpResponse(
            excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="newsletter_subscriptions.xlsx"'
        return response

    export_newsletters_to_csv_action.short_description = "Export selected newsletter subscriptions to CSV"
    export_newsletters_to_excel_action.short_description = "Export selected newsletter subscriptions to Excel"
