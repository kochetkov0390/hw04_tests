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
        cls.user = User.objects.create(username='auth')
        cls.group = Group.objects.create(
            slug='Тестовый слаг'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый текст'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем общедоступные страницы
    def test_home_page_exists_at_correct_location(self):
        """Главная страница доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_page_exists_at_correct_location(self):
        """Страница группы доступна любому пользователю."""
        response = self.guest_client.get('/group/Тестовый слаг/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_page_exists_at_correct_location(self):
        """Профильная страница пользователя доступна любому пользователю."""
        response = self.guest_client.get('/profile/user/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_detail_page_exists_at_correct_location(self):
        """Страница поста доступна любому пользователю."""
        response = self.guest_client.get('/posts/1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Проверяем доступность страниц для авторизованного пользователя
    def test_post_create_page_exists_at_correct_location(self):
        """Cоздание поста доступно только авторизованному пользователю."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_page_exists_at_correct_location(self):
        """Страница редактирования поста доступно только его автору."""
        response = self.authorized_client.get('/posts/1/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Проверка вызываемых шаблонов для каждого адреса
    def test_urls_use_correct_template(self):
        """URL-адрес использует корректный шаблон."""
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/Тестовый слаг/',
            'posts/profile.html': '/profile/user/',
            'posts/post_detail.html': '/posts/1/',
            'posts/post_create.html': '/posts/1/edit/',
            'posts/post_create.html': '/create/',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)

    # Проверяем возврат ошибки 404 при обращении к несуществующей станице
    def test_unexisting_page_returns_404(self):
        """Несуществующая страница вернёт ошибку 404."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
