from django.contrib import admin

from .models import Lesson, Product, Group


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