from django import forms

from .models import ArticleComment

class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ['comment']
        # widgets是小组件的意思
        widgets = {
            'comment': forms.Textarea(attrs={'class':'form-control'}),
        }