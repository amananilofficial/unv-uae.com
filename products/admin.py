from django.contrib import admin
from django.http import HttpResponse
from django.contrib.admin import DateFieldListFilter, SimpleListFilter
from .models import Category, Product, Inquiry, CategorySEO, ProductSEO, Review
from .utils import export_categories_to_csv, export_inquiries_to_csv, export_products_to_csv, export_categories_to_excel, export_inquiries_to_excel, export_products_to_excel, export_reviews_to_csv, export_reviews_to_excel
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class CategorySEOInline(admin.StackedInline):
    model = CategorySEO
    can_delete = False
    verbose_name_plural = 'SEO Information'

    def get_max_num(self, request, obj=None, **kwargs):
        return 1


class ProductSEOInline(admin.StackedInline):
    model = ProductSEO
    can_delete = False
    verbose_name_plural = 'SEO Information'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategorySEOInline]
    list_display = ('name', 'slug', 'description',
                    'created_at', 'get_meta_title')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = [('created_at', DateFieldListFilter)]
    ordering = ('created_at',)
    actions = ['export_categories_to_csv_action',
               'export_categories_to_excel_action']

    def get_meta_title(self, obj):
        return obj.seo.meta_title if hasattr(obj, 'seo') else ''
    get_meta_title.short_description = 'Meta Title'

    def export_categories_to_csv_action(self, request, queryset):
        if 'apply_filter' in request.POST:
            pass
        csv_data = export_categories_to_csv(queryset)
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="categories.csv"'
        return response

    def export_categories_to_excel_action(self, request, queryset):
        excel_file = export_categories_to_excel(queryset)
        response = HttpResponse(
            excel_file,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="categories.xlsx"'
        return response

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            CategorySEO.objects.get_or_create(category=obj)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    inlines = [ProductSEOInline]
    list_display = ('name', 'category', 'stock', 'is_available', 'is_featured',
                    'is_published', 'created_at', 'seo_title', 'seo_rating')
    search_fields = ('name', 'description')
    actions = ['export_products_to_csv_action',
               'export_products_to_excel_action']

    class AvailableFilter(SimpleListFilter):
        title = 'Availability'
        parameter_name = 'availability'

        def lookups(self, request, model_admin):
            return [
                ('True', 'Available'),
                ('False', 'Not Available'),
            ]

        def queryset(self, request, queryset):
            if self.value() == 'True':
                return queryset.filter(is_available=True)
            elif self.value() == 'False':
                return queryset.filter(is_available=False)
            return queryset

    list_filter = [
        ('category', admin.RelatedFieldListFilter),
        AvailableFilter,
        ('created_at', DateFieldListFilter),
        ('is_published', admin.BooleanFieldListFilter),
    ]

    def seo_title(self, obj):
        try:
            return obj.seo.title if hasattr(obj, 'seo') else ''
        except ProductSEO.DoesNotExist:
            return ''

    def seo_rating(self, obj):
        try:
            if hasattr(obj, 'seo'):
                return f"{obj.seo.rating} ({obj.seo.review_count} reviews)"
            return ''
        except ProductSEO.DoesNotExist:
            return ''

    def export_products_to_csv_action(self, request, queryset):
        if 'apply_filter' in request.POST:
            pass
        return self.export_to_csv(queryset, 'products.csv')

    def export_products_to_excel_action(self, request, queryset):
        return self.export_to_excel(queryset, 'products.xlsx')

    def export_to_csv(self, queryset, filename):
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Category', 'Stock',
                        'Is Available', 'Is Featured', 'Created At'])
        for product in queryset:
            writer.writerow([product.id, product.name, product.category.name, product.stock,
                            product.is_available, product.is_featured, product.created_at])
        return response

    def export_to_excel(self, queryset, filename):
        import pandas as pd
        data = []
        for product in queryset:
            data.append({
                'ID': product.id,
                'Name': product.name,
                'Category': product.category.name,
                'Stock': product.stock,
                'Is Available': product.is_available,
                'Is Featured': product.is_featured,
                'Created At': product.created_at,
            })
        df = pd.DataFrame(data)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        df.to_excel(response, index=False)
        return response


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message',
                    'category', 'product', 'created_at')
    search_fields = ('name', 'email', 'message')
    actions = ['export_inquiries_to_csv_action',
               'export_inquiries_to_excel_action']

    class EmailListFilter(admin.SimpleListFilter):
        title = 'Email'
        parameter_name = 'email'

        def lookups(self, request, model_admin):
            return [
                ('@gmail.com', 'Gmail'),
                ('@yahoo.com', 'Yahoo'),
                ('@hotmail.com', 'Hotmail'),
            ]

        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(email__icontains=self.value())
            return queryset

    list_filter = [
        ('created_at', admin.DateFieldListFilter),
        EmailListFilter,
    ]

    def save_inquiry(self, request, form, change):
        inquiry = form.save(commit=False)
        inquiry.save()

    def export_inquiries_to_csv_action(self, request, queryset):
        if 'select_all' in request.POST:
            queryset = Inquiry.objects.all()
        csv_data = export_inquiries_to_csv(queryset)
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inquiries.csv"'

        for inquiry in queryset:
            self.save_inquiry(request, inquiry)

        return response

    def export_inquiries_to_excel_action(self, request, queryset):
        if 'select_all' in request.POST:
            queryset = Inquiry.objects.all()
        excel_file = export_inquiries_to_excel(queryset)
        response = HttpResponse(
            excel_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="inquiries.xlsx"'

        for inquiry in queryset:
            self.save_inquiry(request, inquiry)

        return response

    export_inquiries_to_csv_action.short_description = "Export selected inquiries to CSV"
    export_inquiries_to_excel_action.short_description = "Export selected inquiries to Excel"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'email', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'email', 'review', 'product__name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    actions = ['export_reviews_to_csv_action',
               'export_reviews_to_excel_action']

    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'rating', 'review')
        }),
        ('Reviewer Details', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('created_at',)
        return self.readonly_fields

    def export_reviews_to_csv_action(self, request, queryset):
        if 'select_all' in request.POST:
            queryset = Review.objects.all()
        csv_data = export_reviews_to_csv(queryset)
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reviews.csv"'
        return response

    def export_reviews_to_excel_action(self, request, queryset):
        if 'select_all' in request.POST:
            queryset = Review.objects.all()
        excel_file = export_reviews_to_excel(queryset)
        response = HttpResponse(
            excel_file,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="reviews.xlsx"'
        return response
