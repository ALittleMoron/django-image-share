from django.contrib import admin

from .models import ImageWithContent


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'publisher',
                    'is_published')
    list_display_links = ('id', 'title', 'publisher')
    search_fields = ('title', 'publisher')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'tags')


admin.site.register(ImageWithContent, ImageAdmin)