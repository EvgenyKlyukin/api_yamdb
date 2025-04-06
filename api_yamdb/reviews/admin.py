from django.contrib import admin

from reviews.models import Category, Comments, Genre, GenreTitle, Review, Title

TEXT_RESTRICTION = 50


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


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('title_id', 'author', 'score', 'pub_date')
    list_filter = ('score', 'pub_date')
    search_fields = ('text', 'author__username', 'title__name')
    readonly_fields = ('pub_date',)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'author', 'pub_date', 'short_text')
    list_filter = ('pub_date', 'author')
    search_fields = ('text', 'author__username', 'review__text')
    readonly_fields = ('pub_date',)

    def short_text(self, obj):
        if len(obj.text) > TEXT_RESTRICTION:
            return obj.text[:TEXT_RESTRICTION] + '...'
        else:
            return obj.text
    short_text.short_description = 'Текст'
