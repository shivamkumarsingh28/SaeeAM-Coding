from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import *

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context

    def get_queryset(self):
        ch = get_object_or_404(Category, name=self.kwargs.get('catename'))
       
        return Post.objects.filter(category=ch)
        


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = '__all__'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = '__all__'
    success_url = '/'
    def form_valid(self, form):
        form.instance.author = self.request.user.is_superuser
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = '__all__'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def Main(request):
    que = request.GET.get('search')
    if not que:
        que = "string is empty"
    params = Post.objects.all().filter(title__icontains=que)

    posts = Post.objects.all()
    category = Category.objects.all()
    context = {'posts': posts,  'category':category, 'params': params,
               }

    return render(request, 'blog/main.html',context)
