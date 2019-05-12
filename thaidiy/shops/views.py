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
from django.urls import reverse


def home(request):
    choices = Shop()
    context = {
        # 'shops': Shop.objects.all(),
        'choices': Shop.objects.all(),
    }
    return render(request, 'shops/shops_home.html', context)


class ShopListView(ListView):
    model = Shop
    template_name = 'shops/shops_home.html'
    context_object_name = 'shops'
    # queryset = Shop.objects.values_list('category', flat=True).distinct()
    ordering = ['-date_posted']
    paginate_by = 6


class SidebarListView(ListView):
    model = Shop
    template_name = 'projects/base.html'
    context_object_name = 'shops'


class UserShopListView(ListView):
    model = Shop
    template_name = 'shops/user_shops.html'
    context_object_name = 'shops'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Shop.objects.filter(author=user).order_by('-date_posted')


class CategoryShopListView(ListView):
    model = Shop
    template_name = 'shops/category_shops.html'
    context_object_name = 'shops'
    paginate_by = 6

    def get_queryset(self):
        # cat = get_object_or_404(Shop, category=self.kwargs.get('category'))  # nopep8
        return Shop.objects.filter(category=self.kwargs.get('category')).order_by('-date_posted')  # nopep8


class ShopDetailView(DetailView):
    model = Shop


class ShopCommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']

    def get_context_data(self, **kwargs):
        context = super(ShopCommentCreate, self).get_context_data(**kwargs)
        context['shop'] = get_object_or_404(Shop, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.comment_author = self.request.user
        form.instance.shop = get_object_or_404(Shop, pk=self.kwargs['pk'])
        return super(ShopCommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('shop-detail', kwargs={'pk': self.kwargs['pk']})


class ShopCommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):   # nopep8
    model = Comment
    fields = ['text']
    template_name_suffix = '_update_form'

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def get_success_url(self):
        shop = self.object.shop
        return reverse_lazy('shop-detail', kwargs={'pk': shop.id})


class ShopCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):   # nopep8
    model = Comment

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def get_success_url(self):
        shop = self.object.shop
        return reverse_lazy('shop-detail', kwargs={'pk': shop.id})


class ShopCreateView(LoginRequiredMixin, CreateView):
    model = Shop
    fields = ['name', 'category', 'description', 'details', 'image', 'latitude', 'longitude']  # nopep8

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ShopUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Shop
    fields = ['name', 'category', 'description', 'details', 'image', 'latitude', 'longitude']   # nopep8

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        shop = self.get_object()
        if self.request.user == shop.author:
            return True
        return False


class ShopDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Shop
    success_url = '/'

    def test_func(self):
        shop = self.get_object()
        if self.request.user == shop.author:
            return True
        return False
