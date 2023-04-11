from django.urls import path
from .views import IssueDetailView, IssueListView, CommentDetailView, CommentListView, CommentCreateView, ajax_tag_suggest

urlpatterns = [
    path('issue/<slug:slug>', IssueDetailView.as_view(), name='issue-detail'),
    path('issue/', IssueListView.as_view(), name='issue-list'),
    path('comment/<slug:slug>', CommentDetailView.as_view(), name='comment-detail'),
    path('comment/', CommentListView.as_view(), name='comment-list'),
    path('', CommentCreateView.as_view(), name='comment-create'),
    path('ajax/tags/', ajax_tag_suggest, name='ajax-tags'),
]