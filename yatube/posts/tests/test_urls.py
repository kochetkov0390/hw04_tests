from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = User.objects.create(username='auth')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.test_user,
            group=cls.group,
            text='Тестовый текст',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.test_user)

    # Проверка доступности страниц гостю
    def test_urls_for_guest_client(self):
        """Проверка кодов ответа страниц гостю."""
        status_codes = {
            reverse('posts:index'): HTTPStatus.OK,
            reverse('posts:group_posts',
                    args=[PostURLTest.group.slug]): HTTPStatus.OK,
            reverse('posts:profile',
                    args=[PostURLTest.test_user.username]): HTTPStatus.OK,
            reverse('posts:post_detail',
                    args=[PostURLTest.post.id]): HTTPStatus.OK,
            reverse('posts:post_create'): HTTPStatus.FOUND,
            reverse('posts:post_edit',
                    args=[PostURLTest.post.id]): HTTPStatus.FOUND,
        }
        for page, status_code in status_codes.items():
            with self.subTest(status_code=status_code):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, status_code)

    # Проверка доступности страниц авторизованному пользователю
    def test_urls_for_authorized_client(self):
        """Проверка кодов ответа страниц авторизованному пользователю."""
        status_codes = {
            reverse('posts:index'): HTTPStatus.OK,
            reverse('posts:group_posts',
                    args=[PostURLTest.group.slug]): HTTPStatus.OK,
            reverse('posts:profile',
                    args=[PostURLTest.test_user.username]): HTTPStatus.OK,
            reverse('posts:post_detail',
                    args=[PostURLTest.post.id]): HTTPStatus.OK,
            reverse('posts:post_create'): HTTPStatus.OK,
            reverse('posts:post_edit',
                    args=[PostURLTest.post.id]): HTTPStatus.OK,
        }
        for page, status_code in status_codes.items():
            with self.subTest(status_code=status_code):
                response = self.authorized_client.get(page)
                self.assertEqual(response.status_code, status_code)

    # Проверка возврата ошибки 404
    def test_unexisting_page_returns_404(self):
        """Несуществующая страница вернёт ошибку 404."""
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    # Проверка вызываемых шаблонов
    def test_urls_use_correct_template(self):
        """URL-адрес использует корректный шаблон."""
        templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_posts', args=[PostURLTest.group.slug]):
            'posts/group_list.html',
            reverse('posts:profile',
                    args=[PostURLTest.test_user.username]):
            'posts/profile.html',
            reverse('posts:post_detail', args=[PostURLTest.post.id]):
            'posts/post_detail.html',
            reverse('posts:post_edit', args=[PostURLTest.post.id]):
            'posts/post_create.html',
            reverse('posts:post_create'): 'posts/post_create.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
