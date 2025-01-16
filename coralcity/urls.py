from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView

# Import views
from pages import views as page_views
from products import views as product_views
from contacts import views as contact_views

# Static and media imports
from django.conf.urls.static import static
from django.conf import settings

# Import for sitemap functionality
from django.contrib.sitemaps.views import sitemap
from products.sitemaps import CategorySitemap, ProductSitemap, InquirySitemap
from contacts.sitemaps import InquirySitemap, NewsletterSitemap
from pages.sitemaps import PagesSitemap  # Ensure these modules exist

# Define the sitemaps dictionary
sitemaps = {
    'categories': CategorySitemap,
    'products': ProductSitemap,
    'inquiries': InquirySitemap,
    'inquiries': InquirySitemap,
    'newsletters': NewsletterSitemap,
    'pages': PagesSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('contacts/', include('contacts.urls')),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customize the admin panel appearance
admin.site.site_header = "Uniview | Admin Panel"
admin.site.index_title = "Uniview "
admin.site.site_title = "Control Panel"
