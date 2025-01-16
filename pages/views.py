from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from django.views.generic import ListView, TemplateView
from products.models import Product
from .models import Video, AboutPageVideo


def home(request):
    featured_products = Product.objects.filter(
        is_available=True, is_featured=True).order_by('-created_at')
    context = {
        'featured_products': featured_products,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    try:
        video = AboutPageVideo.objects.filter(is_active=True).first()
        if video and not video.video_url:
            print("Warning: Video found but URL is empty")
            video = None
    except Exception as e:
        print(f"Error fetching video: {e}")
        video = None

    if video:
        print("Debug - Video URL:", video.video_url)  # Log the original URL
        print("Debug - Formatted Video URL:",
              video.formatted_video_url)  # Log the formatted URL
    context = {
        'video': video,
    }
    return render(request, 'pages/about.html', context)


def careers(request):
    return render(request, 'pages/career.html')


def video(request):
    return render(request, 'pages/videos.html')


def solutions(request):
    return render(request, 'pages/solutions.html')


def bank(request):
    return render(request, 'pages/bank.html')


def cookies(request):
    return render(request, 'pages/cookiepolicy.html')


def hospital(request):
    return render(request, 'pages/hospital.html')


def hotel(request):
    return render(request, 'pages/hotel.html')


def school(request):
    return render(request, 'pages/school.html')


def shoppingmall(request):
    return render(request, 'pages/shoppingmall.html')


def stadium(request):
    return render(request, 'pages/stadium.html')


def warehouse(request):
    return render(request, 'pages/warehouse.html')


def building(request):
    return render(request, 'pages/building.html')


def retail(request):
    return render(request, 'pages/retail.html')


def privacy(request):
    return render(request, 'pages/privacy.html')


def video_list(request):
    videos = Video.objects.filter(is_active=True)
    print("Debug - Number of videos:", videos.count())  # Debug print
    for video in videos:
        # Debug print
        print(f"Debug - Video: {video.title}, ID: {video.youtube_id}")

    return render(request, 'pages/videos.html', {'videos': videos})


def about_view(request):
    video = Video.objects.first()  # Fetch the first video or adjust as needed
    return render(request, 'pages/about.html', {'video': video})
