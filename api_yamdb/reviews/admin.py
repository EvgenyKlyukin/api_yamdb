from django.contrib import admin

from reviews.constants import TEXT_RESTRICTION
from reviews.models import Comments


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'pub_date', 'short_text')
    list_filter = ('pub_date', 'author')
    search_fields = ('text', 'author__username', 'review__text')
    readonly_fields = ('pub_date',)

    def short_text(self, obj):
        if len(obj.text) > TEXT_RESTRICTION:
            obj.text[:TEXT_RESTRICTION] + '...'
        else:
            obj.text
    short_text.short_description = 'Текст'
