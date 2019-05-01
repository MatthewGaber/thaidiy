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


def home(request):
    context = {
        'shops': Shop.objects.all(),
    }
    return render(request, 'shops/shops_home.html', context)


class ShopListView(ListView):
    model = Shop
    template_name = 'shops/shops_home.html'
    context_object_name = 'shops'
    ordering = ['-date_posted']
    paginate_by = 5


class UserShopListView(ListView):
    model = Shop
    template_name = 'shops/user_shops.html'
    context_object_name = 'shops'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Shop.objects.filter(author=user).order_by('-date_posted')


class CategoryShopListView(ListView):
    model = Shop
    template_name = 'shops/category_shops.html'
    context_object_name = 'shops'
    paginate_by = 5

    def get_queryset(self):
        # cat = get_object_or_404(Shop, category=self.kwargs.get('category'))  # nopep8
        return Shop.objects.filter(category=self.kwargs.get('category')).order_by('-date_posted')  # nopep8


class ShopDetailView(DetailView):
    model = Shop


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
