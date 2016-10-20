from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from .forms import PostForm, CommentForm
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponseForbidden
from django.core.exceptions import PermissionDenied


class UserDetailView(ListView):
    model = Post
    #template_name = "blog/user_detail.html"

    def get_queryset(self):
        user = User.objects.get(pk=self.kwargs.get("pk"))
        queryset = Post.objects.all().filter(author_id=user).order_by('-create_date')
        query = self.request.GET.get("query")
        if query:
            return Post.objects.filter(text__icontains=query) or Post.objects.filter(title__icontains=query)
        return queryset


class PostsListView(ListView):
    model = Post

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-create_date')
        query = self.request.GET.get("query")
        if query:
            return Post.objects.filter(text__icontains=query) or Post.objects.filter(title__icontains=query)
        return queryset


class PostDetailView(DetailView):
    model = Post

    """def get_object(self):

        #Для неавторизованного пользователя возвращает 404 ошибку

        user = User.objects.get(pk=1)
        object = super(PostDetailView, self).get_object()
        if not self.request.user.is_authenticated():
            raise Http404
        return object
"""


class PrivatePostList(ListView):
    model = Post

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.all().filter(author_id=user).order_by('-create_date')
        query = self.request.GET.get("query")
        if query:
            return Post.objects.filter(text__icontains=query) or Post.objects.filter(title__icontains=query)
        return queryset


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/blog/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "registration/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

"""@login_required
def show_users_posts(request, pk):
    user = User.objects.get(pk=pk)

    if request.user.is_authenticated() and request.user.id == user.id:
        queryset = Post.objects.all().filter(author_id=1).order_by('-create_date')
        query = request.GET.get("query")
        #if query:
            #queryset = Post.objects.filter(text__icontains=query) or Post.objects.filter(title__icontains=query)
        context = {'queryset': queryset}
        return render(request, 'blog/post_list.html', context)

    else:
        raise PermissionDenied"""


@login_required
def post_new(request):
    header = 'Новая запись'
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'header': header})


@login_required
def post_edit(request, pk):
    header = 'Редактировать запись'
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if post.author != request.user:
            raise PermissionDenied
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'header': header})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied
    post.delete()
    return redirect('blog:list')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user;
            comment.save()
            return redirect('blog:detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if comment.post.author != request.user and comment.author != request.user:
        raise PermissionDenied
    comment.delete()
    return redirect('blog:detail', pk=post_pk)



