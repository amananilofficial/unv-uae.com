from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone


class PagesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            'pages:home', 'pages:about', 'pages:careers', 'pages:video', 'pages:solutions', 'pages:bank',
            'pages:cookies', 'pages:hospital', 'pages:hotel', 'pages:school', 'pages:shoppingmall',
            'pages:stadium', 'pages:warehouse', 'pages:building', 'pages:retail'
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return timezone.now()

    def changefreq(self, obj):
        return "monthly"

    def priority(self, obj):
        return 0.5
