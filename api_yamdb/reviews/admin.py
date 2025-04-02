from django.contrib import admin

from .models import Category, Genre, Title, GenreTitle, Reviews


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('year', 'category')


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')
    list_filter = ('genre',)
    

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'score', 'pub_date')
    list_filter = ('score', 'pub_date')
    search_fields = ('text', 'author__username', 'title__name')
    readonly_fields = ('pub_date',)
