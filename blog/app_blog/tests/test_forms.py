from django.test import TestCase

from app_blog import forms


class NewPostFormTest(TestCase):

    def test_form_label(self):
        form = forms.NewPostForm()
        self.assertTrue(form.fields['title'].label == 'Название')
        self.assertTrue(form.fields['text'].label == 'Текст')

    def test_form_values(self):
        form_data = {
            'title': 'тест',
            'slug': 'test',
            'text': 'текст',
        }
        form = forms.NewPostForm(data=form_data)
        self.assertTrue(form.is_valid())