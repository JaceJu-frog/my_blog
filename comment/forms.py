from django import forms

from .models import ArticleComment

# 定义ArticleComment的表单
class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        # 表单中需要传入的参数是comment
        fields = ['comment']
        # widgets是小组件的意思
        widgets = {
            'comment': forms.Textarea(attrs={'class':'form-control'}),
        }