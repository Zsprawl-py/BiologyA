from .models import Course, Module, Subject, Content
from django.contrib import admin


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class ModuleAdmin(admin.StackedInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created',]
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleAdmin]


# @admin.register(Content)
# class ContentAdmin(admin.ModelAdmin):
#     list_display = ['module', 'content_type', 'object_id',]