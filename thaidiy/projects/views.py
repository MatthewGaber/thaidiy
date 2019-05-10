from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy


def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'projects/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'projects/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6


class UserPostListView(ListView):
    model = Post
    template_name = 'projects/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class CategoryPostListView(ListView):
    model = Post
    template_name = 'projects/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        # cat = get_object_or_404(Shop, category=self.kwargs.get('category'))  # nopep8
        return Post.objects.filter(category=self.kwargs.get('category')).order_by('-date_posted')  # nopep8


class PostDetailView(DetailView):
    model = Post


class PostCommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']

    def get_context_data(self, **kwargs):
        context = super(PostCommentCreate, self).get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context
        
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super(PostCommentCreate, self).form_valid(form)

    def get_success_url(self): 
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})


class PostCommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):   # nopep8
    model = Comment
    fields = ['text']
    template_name_suffix = '_update_form'

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def get_success_url(self):
        post = self.object.post
        return reverse_lazy('post-detail', kwargs={'pk': post.id})


class PostCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):   # nopep8
    model = Comment

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def get_success_url(self):
        post = self.object.post
        return reverse_lazy('post-detail', kwargs={'pk': post.id})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'category', 'description', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'category', 'description', 'content']

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


def about(request):
    return render(request, 'projects/about.html', {'title': 'About'})
