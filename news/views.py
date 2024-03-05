from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from datetime import datetime

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from .filters import PostFilter
from .forms import PostForm
from .models import Post


class PostList(ListView):
    model = Post  # Указываем модель, объекты которой мы будем выводить
    ordering = '-post_time'  # Поле, которое будет использоваться для сортировки объектов
    template_name = 'posts.html'   # Указываем имя шаблона, в котором будут все инструкции о том,
    context_object_name = 'posts'  # Это имя списка, в котором будут лежать все объекты.
    paginate_by = 10  # количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NS'
        return super().form_valid(form)


class ArticlesCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AT'
        return super().form_valid(form)


# Добавляем представление для изменения товара.
class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_queryset(self):
        return Post.objects.filter(post_type='NS')


class ArticlesUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_queryset(self):
        return Post.objects.filter(post_type='AT')


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='NS')


class ArticlesDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='AT')


class MyViev(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):

        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context
