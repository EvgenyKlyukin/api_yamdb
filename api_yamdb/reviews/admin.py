from django.contrib import admin

from .models import Category, Genre, GenreTitle, Reviews, Title


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'score', 'pub_date')
    list_filter = ('score', 'pub_date')
    search_fields = ('text', 'author__username', 'title__name')
    readonly_fields = ('pub_date',)
