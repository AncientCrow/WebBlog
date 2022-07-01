from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from app_blog.models import Post


class PostListTest(TestCase):

    def test_url_exist(self):
        response = self.client.get("/blog/", )
        self.assertEqual(response.status_code, 200)

    def test_url_exist_by_name(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)

    def test_view_use_valid_template(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertTemplateUsed(response, "blog/post/list.html")


class PostFilterTest(TestCase):

    def test_url_exist_filter_new(self):
        response = self.client.get('/blog/filter/{}/'.format(1))
        self.assertEqual(response.status_code, 200)

    def test_url_exist_filter_old(self):
        response = self.client.get('/blog/filter/{}/'.format(2), )
        self.assertEqual(response.status_code, 200)

    def test_url_exist_by_name_filter_new(self):
        response = self.client.get(reverse('blog:post_filter', kwargs={'action': 1}))
        self.assertEqual(response.status_code, 200)

    def test_url_exist_by_name_filter_old(self):
        response = self.client.get(reverse('blog:post_filter', kwargs={'action': 2}))
        self.assertEqual(response.status_code, 200)

    def test_url_use_valid_template_name_filter_new(self):
        response = self.client.get(reverse('blog:post_filter', kwargs={'action': 1}))
        self.assertTemplateUsed(response, "blog/post/list.html")

    def test_url_use_valid_template_name_filter_old(self):
        response = self.client.get(reverse('blog:post_filter', kwargs={'action': 2}))
        self.assertTemplateUsed(response, "blog/post/list.html")


class PostReadFilterTest(TestCase):

    def test_url_exist_filter_read(self):
        response = self.client.get('/blog/filter/read/')
        self.assertEqual(response.status_code, 200)

    def test_url_exist_filter_unread(self):
        response = self.client.get('/blog/filter/unread/')
        self.assertEqual(response.status_code, 200)

    def test_url_exist_by_name_filter_read(self):
        response = self.client.get(reverse('blog:post_read_filter', kwargs={'status': 'read'}))
        self.assertEqual(response.status_code, 200)

    def test_url_exist_by_name_filter_unread(self):
        response = self.client.get(reverse('blog:post_read_filter', kwargs={'status': 'unread'}))
        self.assertEqual(response.status_code, 200)

    def test_url_use_valid_template_name_filter_read(self):
        response = self.client.get(reverse('blog:post_read_filter', kwargs={'status': 'read'}))
        self.assertTemplateUsed(response, "blog/post/list.html")

    def test_url_use_valid_template_name_filter_unread(self):
        response = self.client.get(reverse('blog:post_read_filter', kwargs={'status': 'unread'}))
        self.assertTemplateUsed(response, "blog/post/list.html")


class PostDetailTest(TestCase):

    def setUp(self) -> None:
        user = User.objects.create_user(username="test",
                                        email="test@test.ru",
                                        password="123qwe!@#"
                                        )

        self.post = Post.objects.create(
            title='test_title',
            slug='test_title',
            author=User(id=user.id),
            text='test_text',
            published=timezone.now(),
            created=timezone.now(),
            updated=timezone.now(),
            status='published',
        )

    def test_url_exist(self):
        self.client.login(username='test', password='123qwe!@#')
        year, month,  = self.post.published.year, self.post.published.month
        day, slug = self.post.published.day, 'test_title'
        response = self.client.get("/blog/{}/{}/{}/{}/".format(year, month, day, slug))
        self.assertEqual(response.status_code, 200)

    def test_url_exist_by_name(self):
        self.client.login(username='test', password='123qwe!@#')
        response = self.client.get(reverse("blog:post_detail", kwargs={
            'year': self.post.published.year,
            'month': self.post.published.month,
            'day': self.post.published.day,
            'post': self.post.slug
        }))
        self.assertEqual(response.status_code, 200)

    def test_view_use_valid_template(self):
        self.client.login(username='test', password='123qwe!@#')
        response = self.client.get(reverse("blog:post_detail", kwargs={
            'year': self.post.published.year,
            'month': self.post.published.month,
            'day': self.post.published.day,
            'post': self.post.slug
        }))
        self.assertTemplateUsed(response, "blog/post/detail.html")


class NewPostTest(TestCase):

    def test_url_exist(self):
        response = self.client.get('/blog/new_post/')
        self.assertEqual(response.status_code, 200)

    def test_url_exist_by_name(self):
        response = self.client.get(reverse('blog:new_post'))
        self.assertEqual(response.status_code, 200)

    def test_url_use_valid_tempate(self):
        response = self.client.get(reverse('blog:new_post'))
        self.assertTemplateUsed(response, 'blog/post/add.html')


class PostAPITest(TestCase):

    def setUp(self) -> None:
        user = User.objects.create_user(username="test",
                                        email="test@test.ru",
                                        password="123qwe!@#"
                                        )

        self.post = Post.objects.create(
            title='test_title',
            slug='test_title',
            author=User(id=user.id),
            text='test_text',
            published=timezone.now(),
            created=timezone.now(),
            updated=timezone.now(),
            status='published',
        )

    def test_post_api_list_url_exist(self):
        response = self.client.get('/blog/post_api/')
        self.assertEqual(response.status_code, 200)

    def test_post_api_detail_url_exist(self):
        post_id = self.post.id
        response = self.client.get('/blog/post_api/{}/'.format(post_id))
        self.assertEqual(response.status_code, 200)

    def test_post_api_list_url_exist_by_name(self):
        response = self.client.get(reverse('blog:post_api_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_api_detail_url_exist_by_name(self):
        post_id = self.post.id
        response = self.client.get(reverse('blog:post_detail_api', kwargs={'id': post_id}))
        self.assertEqual(response.status_code, 200)