from django.contrib.sitemaps import Sitemap
from .models import Category, Product, Inquiry


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.created_at  # Assuming `created_at` is a good timestamp for lastmod


class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        # Filter only published products
        return Product.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.list_date  # Using `list_date` as the last modification timestamp


class InquirySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Inquiry.objects.all()

    def lastmod(self, obj):
        return obj.created_at  # Use the `created_at` field for lastmod

