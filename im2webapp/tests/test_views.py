import pytest
from django.test import TestCase
from mixer.backend.django import mixer

from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser

from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

from im2webapp.views import (
    HomeView,
    AboutView,
    ImageListView,
    ImageEditorLiteView,
)

from users.views import (
    register,
    profile
)


@pytest.mark.django_db
class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestViews, cls).setUpClass()
        cls.factory = RequestFactory()

    def test_home(self):
        path = reverse('home')
        request = self.factory.get(path)
        view_instance = HomeView.as_view()
        response = view_instance(request)
        assert response.status_code == 200

    def test_about(self):
        path = reverse('about')
        request = self.factory.get(path)
        view_instance = AboutView.as_view()
        response = view_instance(request)
        assert response.status_code == 200

    def test_images_list_authenticated(self):
        path = reverse('images_list')
        request = self.factory.get(path)
        request.user = mixer.blend(User)
        view_instance = ImageListView.as_view()
        response = view_instance(request)
        assert response.status_code == 200

    def test_images_list_unauthenticated(self):
        path = reverse('images_list')
        request = self.factory.get(path)
        request.user = AnonymousUser()
        view_instance = ImageListView.as_view()
        response = view_instance(request)
        assert response.status_code == 302
        assert reverse('login') in response.url

    def test_lite_editor(self):
        path = reverse('lite-editor')
        request = self.factory.get(path)
        view_instance = ImageEditorLiteView.as_view()
        response = view_instance(request)
        assert response.status_code == 200


@pytest.mark.django_db
class TestUserViews(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestUserViews, cls).setUpClass()
        cls.factory = RequestFactory()

    def test_register_get(self):
        path = reverse('register')
        request = self.factory.get(path)
        response = register(request)
        assert response.status_code == 200

    def test_register_post_valid(self):
        path = reverse('register')
        request = self.factory.post(
            path, data={
                'username': 'paulocamargoss',
                'email': 'paulocamargoss@outlook.com',
                'password1': 'hackmehackme',
                'password2': 'hackmehackme',
            }
        )
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        response = register(request)
        assert response.status_code == 302
        assert reverse('login') in response.url

    def test_register_post_invalid(self):
        path = reverse('register')
        request = self.factory.post(
            path, data={
                'username': 'paulocamargoss',
                'email': 'paulocamargoss@outlook.com',
                'password1': 'hackme',
                'password2': 'donthackme',
            }
        )
        response = register(request)
        assert response.status_code == 302
        assert reverse('home') in response.url

    def test_profile_get(self):
        path = reverse('profile')
        request = self.factory.get(path)
        request.user = mixer.blend(User)
        response = profile(request)
        assert response.status_code == 200

    def test_profile_post_valid(self):
        path = reverse('profile')
        request = self.factory.post(
            path, data={
                'username': 'paulocamargoss',
                'email': 'paulocamargoss@outlook.com',
                'image': '',
            }
        )
        request.user = mixer.blend(User)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        response = profile(request)
        assert response.status_code == 302
        assert reverse('profile') in response.url

    def test_profile_post_invalid(self):
        path = reverse('profile')
        request = self.factory.post(
            path, data={
                'username': 'paulocamargoss',
                'email': 'paulocamargoss_outlook.com',
                'image': '',
            }
        )
        request.user = mixer.blend(User)
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        response = profile(request)
        assert response.status_code == 200
