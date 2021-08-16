from django.urls import path

from .views import PostDetail, PostList, SearchPostList, post_share, tag_posts

app_name = "blogs"
urlpatterns = [
    path('', PostList.as_view(), name='list'),
    path('search/', SearchPostList.as_view(), name="search"),
    path('<slug>/', PostDetail, name='detail'),
    path('<slug>/share/', post_share, name='share'),
    path('tag/<slug:tag_slug>/', tag_posts, name='posts_by_tag'),
]
