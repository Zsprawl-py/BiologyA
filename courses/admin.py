from .models import Course, Module, Subject, Content, Team
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

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'email', 'image', 'rule']