# -*- coding:utf-8 -*-
from django.urls import path
from .views import IndexView, PageView, CategoryView, AuthorArticleView, DateHistoryView,\
    SearchView, TagView, MessageBoardView, PublishView

app_name = "blog"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('page/<int:page_id>/', PageView.as_view(), name='detail'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category'),
    path('author/<int:author_id>/', AuthorArticleView.as_view(), name='author'),
    path('date/<slug:date>', DateHistoryView.as_view(), name='date'),
    path('search/', SearchView.as_view(), name='search'),
    path('tag/<str:tag_name>', TagView.as_view(), name='tag'),
    path('message/', MessageBoardView.as_view(), name='message'),
    path('publish/', PublishView.as_view(), name='publish')
]