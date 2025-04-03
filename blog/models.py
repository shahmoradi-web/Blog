import os
import uuid

from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
from django_resized import ResizedImageField
from django_jalali.db import models as jmodels

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)



class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'

    class Category(models.TextChoices):
        WEBSITE = 'وبسایت', 'وبسایت'
        ROBOT = 'رباتیک', 'رباتیک'
        SECURITY = 'امنیت', 'امنیت'
        PROGRAMMING_LANGUAGE = 'زبان برنامه نویسی', 'زبان برنامه نویسی'
        DEVELOPER = 'توسعه دهنده', 'توسعه دهنده'
        NETWORKING = 'شبکه', 'شبکه'
        IOT = 'اینترنت اشیا', 'اینترنت اشیا'
        ARTIFICIAL_INTELLIGENCE = 'هوش مصنوعی', 'هوش مصنوعی'
        TECHNOLOGY = 'تکلونوژی', 'تکلونوژی'
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(max_length=200,blank=True, default=uuid.uuid1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    reading_time = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=200, choices=Category.choices, default=Category.WEBSITE)

    class Meta:
        ordering = ['-published']
        indexes = [models.Index(fields=['published'])]


    # objects = models.Manager()
    objects = models.Manager()
    publish = PublishedManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])


    def __str__(self):
        return self.title


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=200, blank=True, null=True)
    imag_file = ResizedImageField(upload_to='post_images/', size=[500, 500], crop=['top', 'left'], quality=75)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else os.path.basename(self.imag_file.url)


    def delete(self, *args, **kwargs):
        storage, path = self.imag_file.storage, self.imag_file.path
        storage.delete(path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name='متن کامنت')
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')
    active = models.BooleanField(default=False, verbose_name='وضعیت')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f'{self.name} : {self.post}'
