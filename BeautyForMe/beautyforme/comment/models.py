# from django.contrib.auth.models import User
# from django.db import models
# from django.urls import reverse


# class Comment(models.Model):
#     sns = models.ForeignKey('sns.Sns',
#                             on_delete=models.CASCADE,
#                             related_name='comments',
#                             verbose_name='인스타그램')
#     # 작성자와 내용을 저장한다(반복)
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, verbose_name='작성자')
#     content = models.TextField(max_length=100, verbose_name='내용')

#     # 생성일시, 수정일시를 저장한다(반복)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.comment
from django.conf import settings
from django.db import models
from django.urls import reverse

from beautyforme.mixins import Postable, TimeStampedMixin


class Comment(Postable):
    sns = models.ForeignKey('sns.Sns',
                            on_delete=models.CASCADE,
                            related_name='comment',
                            verbose_name='인스타그램')

    def get_absolute_url(self):
        # Instagram feed-list로 리다이렉트한다.
        return reverse('sns:feed-list')
