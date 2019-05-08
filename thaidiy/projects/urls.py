from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CategoryPostListView,
    PostCommentCreate,
)


urlpatterns = [
    path('', PostListView.as_view(), name='projects-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # nopep8
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/',
         PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/',
         PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='projects-about'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('category/<str:category>', CategoryPostListView.as_view(), name='category-posts'),  # nopep8
    path('post/<int:pk>/comment/', PostCommentCreate.as_view(), name='post-comment'),  # nopep8
]
