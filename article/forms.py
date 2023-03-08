# 许多不同类型的数据可能需要在一张表单中准备显示，
# 渲染成HTML，使用方便的界面进行编辑，传到服务器，验证和清理数据，
# 然后保存或跳过进行下一步处理。
# Django的表单功能可以简化上述工作的大部分内容，
# 并且也能比大多数程序员自己编写代码去实现来的更安全。

from django import forms

from .models import ArticlePost

#写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        #指明模型数据来源
        model = ArticlePost
        #指明要显示的字段
        fields = ['title', 'content','column','tags']
