from django.forms import inlineformset_factory  
from photo.models import Album, Photo  
from django import forms 


PhotoInlineFormSet = inlineformset_factory(Album, Photo,
    fields = ['image', 'title', 'description'], 
    extra = 2)

class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='검색어')
