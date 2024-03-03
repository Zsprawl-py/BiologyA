from django.db import models
from django.contrib.auth.models import User
from courses.models import Course


class Article(models.Model):

    TYPES = [
        ("pdf", "PDF"),
        ("book", "BOOK"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    owner = models.ForeignKey(User,
                              related_name='article_created',
                              on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, related_name='articles', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(choices=TYPES)
    file = models.FileField(upload_to='files')

    def __str__(self):
        return self.title

