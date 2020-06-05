from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from photo.models import Category, Photo, Images

class PhotoImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(MPTTModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']


class CategoryAdmin2(DraggableMPTTAdmin):

    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_photos_count', 'related_photos_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Photo,
                'category',
                'photos_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Photo,
                'category',
                'photos_count',
                cumulative=False)
        return qs

    def related_photos_count(self, instance):
        return instance.photos_count
    related_photos_count.short_description = 'Related photos (for this specific category)'

    def related_photos_cumulative_count(self, instance):
        return instance.photos_cumulative_count
    related_photos_cumulative_count.short_description = 'Related photos (in tree)'

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image', 'status']
    list_filter = ['status']
    inlines = [PhotoImageInline]
    #readonly_fields = ('image_tag',)

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']



admin.site.register(Category, CategoryAdmin2)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Images, ImagesAdmin)