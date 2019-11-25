from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    DeleteView,
    CreateView,
    UpdateView
)

from beautyforme.mixins import ValidAuthorRequiredMixin
from comment.models import Comment
from sns.models import Sns


class CommentCreateAjaxView(LoginRequiredMixin, CreateView):
    # 댓글 내용과 분기점을 받아서 적절한 FK를 찾아 연결하고 댓글 목록을 AJAX로 업데이트한다.
    model = Comment
    fields = ['content']
    template_name = 'comment/comment_container.html'

    def form_valid(self, form):
        # 잠깐 db 저장을 멈춘다
        comment = form.save(commit=False)
        # 현재 request를 요청한 user를 댓글의 작성자로 넣어준다
        comment.author = self.request.user
        # 현재 댓글이 달릴 instagram 객체의 pk는 routing rule의 <int:feed_pk>로 넘어온다
        sns = get_object_or_404(Sns, pk=self.kwargs.get('feed_pk'))
        comment.sns = sns
        comment.save()

        context = {
            'comment': Comment.objects
            .select_related('author')
            .filter(sns=sns)
            .order_by('created')
        }

        return render(self.request, 'sns/sns_list.html', context)


class CommentUpdateView(ValidAuthorRequiredMixin, UpdateView):
    model = Comment
    template_name_suffix = '_update_form'
    fields = ['content']
    success_url = '/'

    def get_success_url(self):
        # 현재 Comment의 absolute_url로 리다이렉트 한다.
        return Comment.objects.get(pk=self.kwargs['pk']).get_absolute_url()


class CommentDeleteView(ValidAuthorRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        # 이전 페이지로 이동
        # POST request로 넘어온 'next'인자의 값을 읽어서 success_url로 던져준다
        to = self.request.POST.get('next', '/')
        return to
