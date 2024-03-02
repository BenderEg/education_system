from django.contrib import admin

from .models import Lesson, Product, Group, UserGroup


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'link')
    list_display_links = ('name',)
    ordering = ['name']
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'starting_date', 'creator_id',
                    'price', 'min_students', 'max_students'
                    )
    list_display_links = ('name', 'starting_date', 'creator_id')
    ordering = ['name']
    list_per_page = 20


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    ordering = ['name']
    list_per_page = 20


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'group_id')
    list_display_links = ('user_id', 'group_id')
    list_per_page = 20