from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.db import models


class TimeStampedMixin(models.Model):
    # 생성일시, 수정일시를 저장한다
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Postable(TimeStampedMixin):
    # 자동으로 생성일시, 수정일시 필드가 추가된다
    # 작성자와 내용을 저장한다
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='작성자')
    content = models.TextField(max_length=100, verbose_name='내용')

    class Meta:
        abstract = True


class ValidAuthorRequiredMixin(AccessMixin):
    """상속받은 객체의 author가 운영진이거나 객체의 author가 아니면 403을 반환한다"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # 애초에 로그인을 안했으면 거부한다.
            return self.handle_no_permission()
        elif self.get_object().author != request.user and not request.user.is_staff:
            # 상속받은 객체의 author가 현재 user가 아니고 운영진도 아니라면 거부한다.
            raise PermissionDenied
        else:
            return super(ValidAuthorRequiredMixin, self).dispatch(request, *args, **kwargs)
