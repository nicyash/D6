from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):  # Модель Автор со связью один к одному к встроенным в джанго пользователем
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0)

    def update_rating(self):  # метод обновления рейтинга автора
        posts_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_comments_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'), 0))['pcr']

        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()


class Category(models.Model):  # Жанры
    category = models.CharField(max_length=255, unique=True)


class Post(models.Model):  # Посты с связями один ко многим с авторами и многие с многим с жанрами
    art = 'AT'
    news = 'NS'

    POSITION = [
        (art, 'Статья'),
        (news, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=2, choices=POSITION, default=art)
    post_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255, default='Загаловок')
    text = models.TextField(default='Текст')
    rating = models.IntegerField(default=0)

    def like(self):  # установка лака к посту
        self.rating += 1
        self.save()

    def dislike(self):  # установка дизлайка к посту
        self.rating -= 1
        self.save()

    def preview(self):  # Вывод превью
        small_text = self.text[0:124] + '...'
        return small_text


class PostCategory(models.Model):  # Промежуточная таблица между постами и жанрами
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):  # Коментарии со связями с связями один к многим постам и пользователям
    comment = models.TextField(default='Коментарий')
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def like(self):  # установка лака к коментарию
        self.rating += 1
        self.save()

    def dislike(self):  # установка лака к коментарию
        self.rating -= 1
        self.save()
