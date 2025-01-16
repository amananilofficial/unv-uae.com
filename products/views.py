from django.shortcuts import render, get_object_or_404, redirect
# Ensure all required models are imported
from .models import Category, CategorySEO, Product, Inquiry, Review
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Avg
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail  # Import send_mail function
from django.conf import settings  # Import settings to access email configuration
from django.template.loader import render_to_string  # Import render_to_string


# Display all products
def home(request):
    products = Product.objects.filter(
        is_available=True).order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 6)
    page = request.GET.get('page', 1)
    try:
        paged_products = paginator.page(page)
    except PageNotAnInteger:
        paged_products = paginator.page(1)
    except EmptyPage:
        paged_products = paginator.page(paginator.num_pages)

    context = {'products': paged_products}
    return render(request, 'products/products.html', context)


# Product detail view
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': round(average_rating, 1) if average_rating else 0,
    }
    return render(request, 'products/product_detail.html', context)


# Search functionality
def search(request):
    queryset = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    # Get search parameters from GET request
    keywords = request.GET.get('keywords', '').strip()
    category_name = request.GET.get('category', '').strip()

    # Filter products based on keywords (title or description) and category name
    if keywords:
        queryset = queryset.filter(
            Q(description__icontains=keywords) | Q(title__icontains=keywords)
        )
    if category_name:
        queryset = queryset.filter(category__name__iexact=category_name)

    context = {
        'products': queryset,
        'values': request.GET,  # To preserve search input in form fields
        'categories': categories,
    }
    return render(request, 'products/search.html', context)


# Display products by category
def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(
        category=category, is_available=True).order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 6)
    page = request.GET.get('page', 1)
    try:
        paged_products = paginator.page(page)
    except PageNotAnInteger:
        paged_products = paginator.page(1)
    except EmptyPage:
        paged_products = paginator.page(paginator.num_pages)

    context = {'category': category, 'products': paged_products}
    return render(request, 'products/category.html', context)


# Contact form for product inquiries
def detail_contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        category_id = request.POST.get('category_id')
        product_id = request.POST.get('product_id')

        # Retrieve the product using the product_id
        product = get_object_or_404(Product, id=product_id)

        # Create a new Inquiry instance
        inquiry = Inquiry(
            name=name,
            email=email,
            phone=phone,
            message=message,
            category_id=category_id,
            product_id=product_id
        )
        inquiry.save()  # Save the inquiry to the database

        messages.success(
            request, 'Your inquiry has been submitted successfully!')
        return redirect('products:product_detail', slug=product.slug)

    # If not a POST request, redirect back to the product detail page
    return redirect('products:products')  # Or handle as needed


# Inquiry confirmation page
def inquiry_confirmation(request):
    # Render the inquiry confirmation page after saving the inquiry
    return render(request, 'products/inquiry_confirmation.html')


# All categories view
def all_categories(request):
    categories = Category.objects.all()  # Get all categories
    return render(request, 'products/category.html', {'categories': categories})


# CBV: Product Detail View
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        if hasattr(product, 'seo'):
            context['meta_title'] = product.seo.title
            context['meta_description'] = product.seo.description
            context['meta_keywords'] = product.seo.keywords
            context['rating'] = product.seo.rating
            context['review_count'] = product.seo.review_count
        return context

    def post(self, request, *args, **kwargs):
        # Handle form submission
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        form = Inquiry(request.POST)
        if form.is_valid():
            # Save the form to the database
            contact_inquiry = form.save(commit=False)
            contact_inquiry.product = product  # Associate the inquiry with the product
            contact_inquiry.save()
            return HttpResponse("Your inquiry has been submitted successfully!")
        return render(request, 'products/product_detail.html', {'form': form, 'product': product})


# Get products by category (JSON response)
def get_products_by_category(request, category_id):
    products = Product.objects.filter(category_id=category_id)
    product_data = [{'id': product.id, 'name': product.name}
                    for product in products]
    return JsonResponse({'products': product_data})


# Category view with product count and pagination
def category_view(request, category_id=None):
    categories = Category.objects.annotate(
        product_count=Count('product')
    ).all()

    # Get all available products
    all_products = Product.objects.filter(
        is_available=True).order_by('-created_at')

    # If category_id is provided, filter products by category
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = all_products.filter(category=category)
    else:
        category = None
        products = all_products

    context = {
        'categories': categories,
        'category': category,
        'all_products': products,
        'total_products_count': all_products.count(),
    }
    return render(request, 'products/category.html', context)


# Category detail view (by slug)
def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    return render(request, 'products/category.html', {'category': category})


# Refactored search function (single function only)
def search(request):
    query = request.GET.get('keywords', '')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(id__icontains=query)
        )

    return render(request, 'products/search.html', {'products': products})


class CategoryListView(ListView):
    model = Category
    template_name = 'products/category.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all products - using is_available instead of is_active
        products = Product.objects.filter(
            is_available=True).order_by('-created_at')

        context.update({
            'category': {
                'name': 'All Categories',
                'description': 'Explore our complete collection of product categories'
            },
            'meta_title': 'All Categories - Uniview',
            'meta_description': 'Explore our complete collection of product categories',
            'meta_keywords': 'categories, products, Uniview',
            'all_products': products if products.exists() else [],
        })
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'products/category.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()

        # Get SEO data
        try:
            seo = category.seo
            context['meta_title'] = seo.meta_title or f"{category.name} - Uniview"
            context['meta_description'] = seo.meta_description or category.description
            context['meta_keywords'] = seo.meta_keywords
            context['og_title'] = seo.og_title or context['meta_title']
            context['og_description'] = seo.og_description or context['meta_description']
            context['og_image'] = seo.og_image if seo.og_image else None
            context['canonical_url'] = seo.canonical_url
        except CategorySEO.DoesNotExist:
            # Fallback values if SEO object doesn't exist
            context['meta_title'] = f"{category.name} - Uniview"
            context['meta_description'] = category.description
            context['meta_keywords'] = category.name

        # Get all categories for sidebar
        context['categories'] = Category.objects.filter(is_active=True)

        # Get products for this category
        context['all_products'] = category.products.filter(is_active=True)

        return context


def add_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        Review.objects.create(
            product=product,
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            rating=int(request.POST['rating']),
            review=request.POST['review']
        )
        # Redirect based on user type
        if request.user.is_superuser:  # Check if the user is an admin
            # Use ID for admin
            return redirect('products:product_detail', product_id=product.id)
        else:
            # Use slug for regular users
            return redirect('products:product_detail', slug=product.slug)


def get_all_products(request):
    try:
        products = Product.objects.filter(is_available=True)
        total_count = products.count()

        products_data = [{
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'photo_main': product.photo_main.url if product.photo_main else '',
            'category_name': product.category.name if product.category else '',
        } for product in products]

        return JsonResponse({
            'products': products_data,
            'total_count': total_count,
            'status': 'success'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def toggle_featured_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_featured = not product.is_featured
    product.save()
    return JsonResponse({'is_featured': product.is_featured})


@csrf_protect
def newsletter_subscription(request):
    if request.method == 'POST':
        # Handle the form submission
        # ...
        return redirect('success_url')
    return render(request, 'contacts/newsletter.html')
