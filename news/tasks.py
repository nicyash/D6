import datetime

from celery import shared_task

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category, Subscriber
from django.conf import settings

from datetime import timezone


@shared_task  #  рассылка уведомлений на email подписчиков при создании новости подписанной категории
def send_email_task(pk): #pk надо будет передавать при вызове таски
    post = Post.objects.get(pk=pk)#определяем созданную новость по переданному pk
    subscribers_emails = User.objects.filter(subscriptions__category__in=post.category.all()).values_list('email', flat=True)

    subject = f'Another news has appeared which is concerned with {",".join(category.category for category in post.category.all())}category' #list comprehension («генератора списка»)

    text_content = (
            f'Title: {post.title}\n'
            f'Text: {post.preview()}\n\n'
            f'Url: http://127.0.0.1:8000{post.get_absolute_url()}')

    html_content = (
            f'Title: {post.title}<br>'
            f'Text: {post.preview()}<br><br>'
            f'<a href="http://127.0.0.1{post.get_absolute_url()}">'
            f'Url</a>')

    for email in subscribers_emails:
        msg = EmailMultiAlternatives(subject, text_content, from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task #рассылка уведомлений на email подписчиков о созданных за последние 7 дней новостях подписанной категории
def weekly_send_email_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_time__gte=last_week)
    categories = set(posts.values_list('category__category', flat=True))
    subscribers = set(Category.objects.filter(category__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
