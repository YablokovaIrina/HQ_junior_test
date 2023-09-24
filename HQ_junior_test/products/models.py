from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)
    lesson = models.ManyToManyField('Lesson', related_name='lesson')

    def __str__(self):
        return self.name[:20]


class Lesson(models.Model):
    product = models.ManyToManyField(Product, related_name='product')
    title = models.CharField(max_length=255)
    video_link = models.URLField()
    duration = models.IntegerField()

    def __str__(self):
        return self.title[:20]


class ProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed_time = models.IntegerField()
    is_viewed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} {self.lesson}'
