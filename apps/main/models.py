import string
import random

from django.db import models as db
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class Visitor(db.Model):
    ip = db.CharField(max_length=100, verbose_name='Ip')

    class Meta:
        verbose_name = 'Visitors'
        verbose_name_plural = verbose_name


class Profile(db.Model):
    user = db.OneToOneField(User, on_delete=db.CASCADE)
    bio = db.TextField(max_length=500, blank=True)
    location = db.CharField(max_length=30, blank=True)
    birth_date = db.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Article(db.Model):
    title = db.CharField("Название", max_length=50)
    text = db.TextField("Описание")
    url = db.SlugField("Ссылка", max_length=60, unique=True)
    draft = db.BooleanField("Черновик", default=False)
    author = db.ForeignKey(
        User, verbose_name = "Имя ползователя", on_delete=db.SET_NULL, null=True
    )

    created_date = db.DateTimeField("Дата")


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if not self.url:
            self.url = slugify(rand_slug() + "-" + self.title)
        super(Article, self).save(*args, **kwargs)


    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"