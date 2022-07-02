from django import forms


class NewPostForm(forms.Form):

    title = forms.CharField(max_length=200, label='Название')
    text = forms.CharField(widget=forms.TextInput, label='Текст')


