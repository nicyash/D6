from django.contrib import admin
from .models import Post, Author, Category


def nullfy_quantity(modeladmin, request, queryset): # самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(text='')


# описание для более понятного представления в админ панеле задаётся, как будто это объект
nullfy_quantity.short_description = 'Удалить текст статьи'


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # list_display = [field.name for field in Product._meta.get_fields()] # генерируем список имён всех полей для более красивого отображения
    list_display = ('author', 'title', 'post_type')
    list_filter = ('title', 'category', 'author')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'text')  # тут всё очень похоже на фильтры из запросов в базу
    actions = [nullfy_quantity]  # добавляем действия в список


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Category)
