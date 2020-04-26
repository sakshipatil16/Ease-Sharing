from django import forms
from .models import Item,Comment

class ItemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=('title','price','discount_price','category','description','image','contact')



class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)
