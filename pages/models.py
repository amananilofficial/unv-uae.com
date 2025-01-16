from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class Video(models.Model):
    title = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=20)
    upload_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def youtube_url(self):
        return f"https://www.youtube-nocookie.com/embed/{self.youtube_id}"

    @property
    def thumbnail_url(self):
        return f"https://img.youtube.com/vi/{self.youtube_id}/0.jpg"


class AboutPageVideo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField(help_text="Enter the YouTube video URL")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Ensure only one video is active at a time
        if self.is_active:
            AboutPageVideo.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    @property
    def formatted_video_url(self):
        """Returns a properly formatted embed URL"""
        url = self.video_url
        if not url:
            return ''
        
        # Extract video ID
        video_id = ''
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('watch?v=')[1].split('&')[0]
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
        elif 'youtube.com/embed/' in url:
            video_id = url.split('embed/')[1].split('?')[0]
        else:
            video_id = url.strip()
        
        # Return the embed URL with necessary parameters
        return f'https://www.youtube.com/embed/{video_id}?autoplay=1&rel=0&enablejsapi=1'

    class Meta:
        verbose_name = "About Page Video"
        verbose_name_plural = "About Page Videos"

    def __str__(self):
        return self.title

    def clean(self):
        if self.video_url:
            validator = URLValidator()
            try:
                validator(self.video_url)
            except ValidationError:
                raise ValidationError(
                    {'video_url': 'Please enter a valid URL'})

            # Validate it's a YouTube URL
            if not ('youtube.com' in self.video_url or 'youtu.be' in self.video_url):
                raise ValidationError(
                    {'video_url': 'Please enter a valid YouTube URL'})
