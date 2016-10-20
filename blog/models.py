# -*- coding: utf-8 -*-
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey('auth.User', default="")
    title=models.CharField(u'Заголовок', max_length=150)
    text=models.TextField(u'Текст')
    create_date=models.DateTimeField(u'Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = u'Запись в блоге'
        verbose_name_plural = u'Записи в блоге'
        ordering = ['-create_date']

    def __unicode__(self):
        return self.title

    def __str__(self):
        return u'{}{}'.format(self.title, self.create_date)

    def get_absolute_url(self):
        return "/blog/%i/" % self.id


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


