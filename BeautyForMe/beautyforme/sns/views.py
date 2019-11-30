from urllib.parse import urlparse
from django.http import HttpResponseForbidden, HttpResponse
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormMixin
from django.views.generic.detail import DetailView
from .models import Sns
from django.template import loader
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from comment.forms import CommentForm
from django.contrib import messages
from django.db.models import Count


class SnsList(FormMixin, ListView):
    form_class = CommentForm
    model = Sns
    template_name_suffix = '_list'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated is False:
            return redirect('accounts:login')
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # superclass의 get_context_data를 부른다
        context = super(SnsList, self).get_context_data(**kwargs)
        # CommentForm을 context_data에 넣어준다
        context['comment_form'] = self.get_form()
        return context


def upload_file(request):
    print("----------------------")

    return redirect('/sns')


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
            return redirect('/sns')
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


class SnsDetail(FormMixin, ListView):
    form_class = CommentForm
    model = Sns
    template_name_suffix = '_list'

    def get_context_data(self, **kwargs):
        # superclass의 get_context_data를 부른다
        context = super(SnsDetail, self).get_context_data(**kwargs)
        # CommentForm을 context_data에 넣어준다
        context['comment_form'] = self.get_form()
        return context


class SnsLike(View):
    def post(self, request, *args, **kwargs):
        print(kwargs)
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
    template_name = 'sns/sns_ranking.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return redirect('accounts:login')
        return super(SnsLikeList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # user = self.request.user
        # queryset = user.like_post.all().order_by("-like")[0:5]
        queryset = Sns.objects.annotate(
            q_count=Count('like')).order_by('-q_count')[0:5]
        # print(queryset[0].like(user=self.request.user))
        print(queryset)

        return queryset


class SnsFavoriteList(FormMixin, ListView):
    form_class = CommentForm
    model = Sns
    template_name = 'sns/sns_list.html'

    def get_context_data(self, **kwargs):
        # superclass의 get_context_data를 부른다
        context = super(SnsFavoriteList, self).get_context_data(**kwargs)
        # CommentForm을 context_data에 넣어준다
        context['comment_form'] = self.get_form()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')
        return super(SnsFavoriteList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # 내가 좋아요한 글을 보여주
        user = self.request.user
        queryset = user.like_post.all()
        print(queryset)
        return queryset


class SnsMyList(ListView):
    model = Sns
    template_name = 'sns/sns_mylist.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # 로그인확인
            messages.warning(request, '로그인을 먼저하세요')
            return HttpResponseRedirect('/')

        return super(SnsMyList, self).dispatch(request, *args, **kwargs)


def ranking(request):
    snss = Sns.objects.all()
    template = loader.get_template('sns/sns_rangkingmylist.html')
    context = {
        'object_list': snss,
        'name': request.POST['next'],
    }
    return HttpResponse(template.render(context, request))
