from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def setUp(self):
        self.guest_client = Client()
        self.test_user = User.objects.create_user(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.test_user)

    def test_post_create(self):
        """Отправка валидной формы создаёт пост."""
        posts_count = Post.objects.count()
        form_data = {
            'group': self.group.id,
            'text': 'Тестовый текст',
            'author': self.test_user,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        last_post = Post.objects.last()
        self.assertEqual(last_post.text, form_data['text'])
        self.assertEqual(last_post.group.id, form_data['group'])
        self.assertEqual(last_post.author, form_data['author'])

    def test_edit_post(self):
        """Отправка валидной формы редактирует пост."""
        post = Post.objects.create(
            group=self.group,
            text='Тестовый текст',
            author=self.test_user,
        )
        posts_count = Post.objects.count()
        edited_text = 'Отредактированный тестовый текст'
        form_data = {
            'group': self.group.id,
            'text': edited_text,
            'author': self.authorized_client,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post.id, }),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), posts_count)
        edited_post = Post.objects.get(id=post.id)
        self.assertEqual(edited_post.text, form_data['text'])
        self.assertEqual(edited_post.group.id, form_data['group'])

    def test_guest_can_create_posts(self):
        """Проверка невозможности создания поста гостем."""
        posts_count = Post.objects.count()
        form_data = {
            'group': self.group.id,
            'text': 'Тестовый текст',
            'author': self.guest_client,
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, '/auth/login/?next=/create/')
        self.assertEqual(Post.objects.count(), posts_count)
