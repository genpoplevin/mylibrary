from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'library:book_list_by_category', args=[self.slug]
        )


class Book(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='books',
        on_delete=models.CASCADE
    )
    author = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    slug = models.SlugField(max_length=200)
    image = models.ImageField(
        upload_to='books/%Y/%m/%d',
        blank=True
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'library:book_detail',
            args=[self.id, self.slug]
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='following',
    )

    def __str__(self):
        return f'{self.user} подписан на книгу {self.book}'
