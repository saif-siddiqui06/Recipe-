from django import forms
from .models import Recipe, Comment, Rating

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'cooking_time']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        widgets = {'value': forms.RadioSelect(attrs={'class': 'rating-radio'})}
