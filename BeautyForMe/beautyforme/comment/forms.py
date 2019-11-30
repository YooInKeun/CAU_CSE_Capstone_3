from django.forms import ModelForm

from comment.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        # 최대한 Instagram과 비슷하게 스타일링한다
        self.fields['content'].widget.attrs['class'] = 'textfield-comment'
        self.fields['content'].widget.attrs['placeholder'] = '댓글 달기...'
        self.fields['content'].label = ''
