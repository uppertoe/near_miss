from django.db.models import Count
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from django.views.generic import DetailView, ListView, CreateView
from .models import Issue, Comment


class IssueDetailView(DetailView):
    model = Issue
    context_object_name = 'issue'
    template_name = 'issues/issue_detail.html'
    queryset = (Issue.objects.all()
                .exclude(active=False))


class IssueListView(ListView):
    model = Issue
    context_object_name = 'issue_list'
    template_name = 'issues/issue_list.html'
    queryset = (Issue.objects
                .exclude(active=False)
                .annotate(comment_count=Count('comments'))
                .order_by('-comment_count')[:5])
    

class CommentDetailView(DetailView):
    model = Comment
    context_object_name = 'comment'
    template_name = 'issues/comment_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = self.object.issues.all()
        return context


class CommentListView(ListView):
    model = Comment
    context_object_name = 'comment_list'
    template_name = 'issues/comment_list.html'
    queryset = Comment.objects.all().order_by('-created')


class CommentCreateView(CreateView):
    model = Comment
    fields = ['text']
    template_name = 'issues/comment_create_form.html'
    success_url = reverse_lazy('comment-list')


def ajax_tag_suggest(request):

    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponseBadRequest('Bad Request')
    
    if request.method == 'GET':
        top_tags = (Issue.objects
                    .exclude(active=False)
                    .annotate(comment_count=Count('comments'))
                    .order_by('-comment_count')[:5])
        issues = Issue.all_issues_list()
        context = {'status': 'success',
                   'issues': issues,
                   #'top_tags': top_tags,
                   }
        return JsonResponse(context, status=200)
    
    return JsonResponse({'status': 'bad request'}, status=400)
