
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from gjango.urls import resolve, reverse

from ..forms import PostForm
from ..models import Group, Post

User = get_user_model()
    
    

        cls.group = Group.objects.create(
            title='Тестовая группа'
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.form = Post.Form()
    
    def test_create_post(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': 'Тестовая группа',
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('posts:profile', kwargs={'username': 'Author'})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                group='Тестовая группа'
            ).exists()
        )
