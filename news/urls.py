from django.urls import path
# Импортируем созданное нами представление
from .views import (PostList, PostDetail, PostCreate, PostUpdate, PostDelete,
                    MyViev, ArticlesCreate, ArticlesUpdate, ArticlesDelete, CategoriesListView, subscribe)


urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', PostList.as_view()),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', PostDetail.as_view()),

    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', MyViev.as_view(), name='post_list_fil'),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='post_update'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='post_delete'),
    path('categories/<int:pk>', CategoriesListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe' )

]
