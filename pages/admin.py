from django.contrib import admin
from .models import Video, AboutPageVideo

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'youtube_id', 'upload_date', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('title',)
    list_filter = ('is_active', 'upload_date')
    prepopulated_fields = {'slug': ('title',)}



@admin.register(AboutPageVideo)
class AboutPageVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_url', 'is_active', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'video_url')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'video_url', 'is_active')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

