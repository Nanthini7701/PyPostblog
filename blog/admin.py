from django.contrib import admin
from django.utils.html import mark_safe
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published", "created_at", "image_preview")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" '
                f'style="max-height:60px;border-radius:6px;" />'
            )
        return "(No image)"
    image_preview.short_description = "Image"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at", "edited")
