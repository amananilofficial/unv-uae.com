from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Product, Category

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_available=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/products/{obj.category.slug}/{obj.slug}/"

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Category.objects.filter(is_active=True)

    def location(self, obj):
        return f"/category/{obj.slug}/" 