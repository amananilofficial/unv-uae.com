from django.db import models
from datetime import datetime
from django.utils.text import slugify
from django.urls import reverse
from meta.models import ModelMeta
from django.utils.safestring import mark_safe
from cloudinary_storage.storage import RawMediaCloudinaryStorage
# Category Model


class CategorySEO(models.Model):
    category = models.OneToOneField(
        'Category', on_delete=models.CASCADE, related_name='seo')
    meta_title = models.CharField(
        max_length=60, blank=True, help_text="Max 60 characters for optimal SEO")
    meta_description = models.TextField(
        max_length=160, blank=True, help_text="Max 160 characters for optimal SEO")
    meta_keywords = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated keywords")
    og_title = models.CharField(
        max_length=60, blank=True, help_text="Open Graph title")
    og_description = models.TextField(
        max_length=200, blank=True, help_text="Open Graph description")
    og_image = models.ImageField(upload_to='category/og-images/', blank=True)
    canonical_url = models.URLField(
        blank=True, help_text="Canonical URL if different from default")

    class Meta:
        verbose_name = "Category SEO"
        verbose_name_plural = "Category SEOs"

    def __str__(self):
        return f"SEO for {self.category.name}"


class Category(models.Model, ModelMeta):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, default='default-slug')
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='category/%Y/%m/%d/',
        blank=True,
        null=True,
        storage=RawMediaCloudinaryStorage()
    )
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Assuming you have a URL pattern named 'category_detail' for categories
        return reverse('products:category_detail', kwargs={'slug': self.slug})

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" />')
        return ''

    class Meta:
        ordering = ['name']

# Product Model


class ProductSEO(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.PositiveIntegerField(default=0)
    product = models.OneToOneField(
        'Product', on_delete=models.CASCADE, related_name='seo')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product SEO"
        verbose_name_plural = "Product SEOs"


class Product(models.Model, ModelMeta):
    # Basic Information
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    # Camera Specifications
    max_resolution = models.CharField(max_length=100, blank=True, null=True)
    sensor = models.CharField(max_length=100, blank=True, null=True)
    day_night = models.CharField(max_length=100, blank=True, null=True)
    shutter = models.CharField(max_length=100, blank=True, null=True)
    adjustment_angle = models.CharField(max_length=100, blank=True, null=True)
    s_n = models.CharField(max_length=100, blank=True, null=True)
    wdr = models.CharField(max_length=100, blank=True, null=True)

    # Lens Specifications
    focal_length = models.CharField(max_length=100, blank=True, null=True)
    iris_type = models.CharField(max_length=100, blank=True, null=True)
    iris = models.CharField(max_length=100, blank=True, null=True)
    lens_type = models.CharField(max_length=100, blank=True, null=True)

    # Video Specifications
    video_compression = models.CharField(max_length=100, blank=True, null=True)
    frame_rate = models.CharField(max_length=100, blank=True, null=True)
    video_bit_rate = models.CharField(max_length=100, blank=True, null=True)
    video_stream = models.CharField(max_length=100, blank=True, null=True)
    ip_video_input = models.CharField(max_length=100, blank=True, null=True)
    recording_resolution = models.CharField(
        max_length=100, blank=True, null=True)

    # Audio Specifications
    audio_compression = models.CharField(max_length=100, blank=True, null=True)
    audio_bitrate = models.CharField(max_length=100, blank=True, null=True)
    two_way_audio = models.CharField(max_length=100, blank=True, null=True)
    suppression = models.CharField(max_length=100, blank=True, null=True)
    sampling_rate = models.CharField(max_length=100, blank=True, null=True)
    rca_audio_output = models.CharField(max_length=100, blank=True, null=True)

    # Storage
    edge_storage = models.CharField(max_length=100, blank=True, null=True)
    network_storage = models.CharField(max_length=100, blank=True, null=True)
    sata = models.CharField(max_length=100, blank=True, null=True)

    # Network
    protocols = models.CharField(max_length=100, blank=True, null=True)
    compatible_integration = models.CharField(
        max_length=100, blank=True, null=True)
    incoming_bandwidth = models.CharField(
        max_length=100, blank=True, null=True)
    outgoing_bandwidth = models.CharField(
        max_length=100, blank=True, null=True)
    network_interface = models.CharField(max_length=100, blank=True, null=True)
    poe = models.CharField(max_length=100, blank=True, null=True)

    # Output Interfaces
    hdmi_video_output = models.CharField(max_length=100, blank=True, null=True)
    vga_video_output = models.CharField(max_length=100, blank=True, null=True)
    hdmi_audio_output = models.CharField(max_length=100, blank=True, null=True)
    vga_audio_output = models.CharField(max_length=100, blank=True, null=True)

    # General Specifications
    power = models.CharField(max_length=100, blank=True, null=True)
    dimensions = models.CharField(max_length=100, blank=True, null=True)
    weight = models.CharField(max_length=100, blank=True, null=True)
    material = models.CharField(max_length=100, blank=True, null=True)
    decoding_format = models.CharField(max_length=100, blank=True, null=True)

    # Images
    photo_main = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        blank=True,
        null=True,
        # storage=RawMediaCloudinaryStorage()
    )
    photo_1 = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        blank=True,
        null=True,
        # storage=RawMediaCloudinaryStorage()
    )
    photo_2 = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        blank=True,
        null=True,
        # storage=RawMediaCloudinaryStorage()
    )
    photo_3 = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        blank=True,
        null=True,
        # storage=RawMediaCloudinaryStorage()
    )
    photo_4 = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        blank=True,
        null=True,
        # storage=RawMediaCloudinaryStorage()
    )

    # Metadata
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    is_available = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    is_mvp = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    _meta_title = 'name'
    _meta_description = 'description'
    _meta_image = 'photo_main'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name  # Changed to 'name' instead of 'title'

    def get_absolute_url(self):
        # Assuming you have a URL pattern named 'product_detail' for products
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']

# Inquiry Model


class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, default='No phone number provided')
    message = models.TextField(default='No message provided')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Add this model to your existing models.py


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Review by {self.name} for {self.product.name}'
