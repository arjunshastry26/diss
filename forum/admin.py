from django.contrib import admin
from .models import Category, Discussion, Comment, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'is_resolved', 'views')
    list_filter = ('category', 'is_resolved')
    search_fields = ('title', 'body')
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('discussion', 'author', 'created_at', 'is_solution')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'joined_on')
