from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.conf import settings

from BiologyA.settings.base import PrivateMediaStorage, ImageStorage, FileStorage


class Team(models.Model):
    RULES = [
        ("instructor", "INSTRUCTOR"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(storage=ImageStorage(), blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    rule = models.CharField(choices=RULES, max_length=200, blank=True, null=True)
    # courses = models.ForeignKey(Course, related_name='instructor', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(User,
                              related_name='course_created',
                              on_delete=models.CASCADE)
    instructor = models.ForeignKey(Team, related_name='courses', on_delete=models.CASCADE, blank=True, null=True)
    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      # on_delete=models.CASCADE,
                                      blank=True)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.CharField()
    created = models.DateTimeField(auto_now_add=True)
    # photo = models.FileField(storage=ImageStorage(), blank=True, null=True)
    photo = models.ImageField(storage=ImageStorage(), blank=True, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':('text', 'image', 'video', 'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self})


class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    # content = models.FileField(upload_to='files')
    content = models.FileField(storage=FileStorage(), blank=True, null=True)

class Image(ItemBase):
    # files = models.FileField(upload_to='images')
    images = models.FileField(storage=ImageStorage(), blank=True, null=True)

class Video(ItemBase):
    # url = models.URLField(null=True, blank=True)
    videos = models.FileField(storage=PrivateMediaStorage(), blank=True, null=True)
