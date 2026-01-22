from django import forms
from shop.models import Rating


class RatingForm(forms.ModelForm):
    class Meta :
        model =Rating
        fields = ['rating','comment']
        
        widgets = {
           'rating':forms.Select(choices=[(i,i)for i in range (1,6)]),
           'comment':forms.Textarea(attrs={'rows':4})
       } 
