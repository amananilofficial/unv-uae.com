from django.urls import path
from . import views
from .views import CategoryListView, CategoryDetailView

app_name = 'products'

urlpatterns = [
    path('', views.home, name='products'),  # FBV to display all products
    path('category/', CategoryListView.as_view(), name='category_list'),  # Updated to CBV
    path('category/<int:category_id>/', views.category_view, name='category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),  # Use slug here
    path('search/', views.search, name='search'),  # FBV for searching products
    path('product/<slug:slug>/contact/', views.detail_contact_form, name='detailcontactform'),  # Example pattern
    path('inquiry-confirmation/', views.inquiry_confirmation, name='inquiry_confirmation'),  # FBV for confirmation page
    path('get-products-by-category/<int:category_id>/', views.get_products_by_category, name='get_products_by_category'),
    path('category/', views.all_categories, name='all_category'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),  # Updated to CBV
    path('product/<int:product_id>/add-review/', views.add_review, name='add_review'),
    path('get-all-products/', views.get_all_products, name='get_all_products'),
    path('product/<int:product_id>/toggle-featured/', views.toggle_featured_product, name='toggle_featured_product'),
    path('contact/', views.detail_contact_form, name='contact'),
    path('inquiry/', views.detail_contact_form, name='detail_contact_form'),
]
