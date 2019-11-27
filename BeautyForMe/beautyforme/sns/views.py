from urllib.parse import urlparse
from django.http import HttpResponseForbidden
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormMixin
from django.views.generic.detail import DetailView
from .models import Sns

from django.http import HttpResponseRedirect
from comment.forms import CommentForm
from django.contrib import messages


class SnsList(FormMixin, ListView):
    form_class = CommentForm
    model = Sns
    template_name_suffix = '_list'

    def get_context_data(self, **kwargs):
        # superclass의 get_context_data를 부른다
        context = super(SnsList, self).get_context_data(**kwargs)
        # CommentForm을 context_data에 넣어준다
        context['comment_form'] = self.get_form()
        return context

# class CommentCreateView(CreateView):
#     model = Comment
#     fields = ['content']
#     # TODO: 템플릿 작성
#     template_name = 'sns/zzz.html'
#     print("dddsd")

#     def form_valid(self, form):
#         # 잠깐 db 저장을 멈춘다
#         print(form)
#         comment = form.save(commit=False)
#         print("dd")
#         # 현재 request를 요청한 user를 댓글의 작성자로 넣어준다
#         comment.author = self.request.user

#         # 현재 댓글이 달릴 sns 객체의 pk는 의 <int:feed_pk>로 넘어온다
#         comment.sns = Sns.objects.get(
#             pk=self.kwargs.get('feed_pk'))
#         comment.save()
#         # 댓글을 생성한 이후 댓글을 달고 있었던 request url로 리다이렉트한다.
#         return HttpResponseRedirect(self.request.POST.get('next', '/'))


class SnsCreate(CreateView):
    model = Sns
    fields = ['text', 'image']
    template_name_suffix = '_create'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            # 올바르다면
            # form : 모델폼
            form.instance.save()
            return redirect('/')
        else:
            # 올바르지 않다면
            return self.render_to_response({'form': form})


class SnsUpdate(UpdateView):
    model = Sns
    fields = ['text', 'image']
    template_name_suffix = '_update'
    # success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(SnsUpdate, self).dispatch(request, *args, **kwargs)


class SnsDelete(DeleteView):
    model = Sns
    template_name_suffix = '_delete'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(SnsDelete, self).dispatch(request, *args, **kwargs)


class SnsDetail(DetailView):
    model = Sns
    template_name_suffix = '_detail'


class SnsLike(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            return HttpResponseForbidden()
        else:
            if 'sns_id' in kwargs:
                sns_id = kwargs['sns_id']
                sns = Sns.objects.get(pk=sns_id)
                user = request.user
                if user in sns.like.all():
                    sns.like.remove(user)
                else:
                    sns.like.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)


class SnsFavorite(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            return HttpResponseForbidden()
        else:
            if 'sns_id' in kwargs:
                sns_id = kwargs['sns_id']
                sns = Sns.objects.get(pk=sns_id)
                user = request.user
                if user in sns.favorite.all():
                    sns.favorite.remove(user)
                else:
                    sns.favorite.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)


class SnsLikeList(ListView):
    model = Sns
    template_name = 'sns/sns_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(SnsLikeList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # 내가 좋아요한 글을 보여주
        user = self.request.user
        queryset = user.like_post.all()
        return queryset


class SnsFavoriteList(ListView):
    model = Sns
    template_name = 'sns/sns_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(SnsFavoriteList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # 내가 좋아요한 글을 보여주기
        user = self.request.user
        queryset = user.favorite_post.all()
        return queryset


class SnsMyList(ListView):
    model = Sns
    template_name = 'sns/sns_mylist.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(SnsMyList, self).dispatch(request, *args, **kwargs)
