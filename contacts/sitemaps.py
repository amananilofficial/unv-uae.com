from django.contrib.sitemaps import Sitemap
from .models import Inquiry, NewsletterSubscription


class InquirySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Inquiry.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # Ensure the `Inquiry` model has the `updated_at` field


class NewsletterSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return NewsletterSubscription.objects.all()

    def lastmod(self, obj):
        # Ensure the `NewsletterSubscription` model has the `updated_at` field
        return obj.updated_at
