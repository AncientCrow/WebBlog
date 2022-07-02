from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from app_blog.models import Post


class PostTest(TestCase):

    def setUp(self) -> None:
        user = User.objects.create_user(username="test",
                                        email="test@test.ru",
                                        password="123qwe!@#"
                                        )

        self.post = Post.objects.create(
            title='text',
            author=user,
            text='test_text',
            published=timezone.now(),
            created=timezone.now(),
            updated=timezone.now(),
            status='published',
        )
        self.post.read_status.add(user.id)

    def test_absolute_url(self):
        year, month = self.post.published.year, self.post.published.month
        day, post = self.post.published.day, self.post.slug
        self.assertEqual(self.post.get_absolute_url(), '/{}/{}/{}/{}/'.format(year, month, day, post))

    def test_title_max_length(self):
        post = Post.objects.get(id=self.post.id)
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_slug_max_length(self):
        post = Post.objects.get(id=self.post.id)
        max_length = post._meta.get_field('slug').max_length
        self.assertEqual(max_length, 200)

    def test_status_max_length(self):
        post = Post.objects.get(id=self.post.id)
        max_length = post._meta.get_field('status').max_length
        self.assertEqual(max_length, 30)

    def test_status_choices(self):
        post = Post.objects.get(id=self.post.id)
        choices = post._meta.get_field('status').choices
        # формат выбора ('published', 'Опубликовано')
        for elements in choices:
            self.assertTrue(elements[0] in ('draft', 'moderation', 'published'))


