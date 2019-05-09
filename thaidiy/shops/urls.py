from django.urls import path
from . import views
from .views import (
    ShopListView,
    ShopDetailView,
    ShopCreateView,
    ShopUpdateView,
    ShopDeleteView,
    UserShopListView,
    CategoryShopListView,
    ShopCommentCreate,
    )


urlpatterns = [
    path('', ShopListView.as_view(), name='shops-home'),
    path('shops/<int:pk>/', ShopDetailView.as_view(), name='shop-detail'),
    path('shops/new/', ShopCreateView.as_view(), name='shop-create'),
    path('shops/<int:pk>/update/',
         ShopUpdateView.as_view(), name='shop-update'),
    path('shops/<int:pk>/delete/',
         ShopDeleteView.as_view(), name='shop-delete'),
    path('user/<str:username>', UserShopListView.as_view(), name='user-shops'),
    path('category/<str:category>', CategoryShopListView.as_view(), name='category-shops'),  # nopep8
    path('shop/<int:pk>/comment/', ShopCommentCreate.as_view(), name='shop-comment'),  # nopep8
         ]
