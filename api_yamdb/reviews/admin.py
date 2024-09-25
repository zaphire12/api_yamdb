from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
    ordering = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
    ordering = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category')
    search_fields = ('name', 'year', 'category__name')
    list_filter = ('year', 'category')
    ordering = ('name',)
    filter_horizontal = ('genre',)


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre', 'title')
    search_fields = ('genre__name', 'title__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'score', 'pub_date')
    search_fields = ('title__name', 'author__username', 'score')
    list_filter = ('score', 'pub_date')
    ordering = ('pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review_id', 'author', 'pub_date')
    search_fields = ('review_id__text', 'author__username')
    list_filter = ('pub_date',)
    ordering = ('pub_date',)
