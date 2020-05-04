from django.urls import reverse, resolve


class TestUrls:
    def home_url(self):
        path = reverse('home')
        assert resolve(path).view_name == 'home'

    def about_url(self):
        path = reverse('about')
        assert resolve(path).view_name == 'about'

    def lite_editor_url(self):
        path = reverse('lite-editor')
        assert resolve(path).view_name == 'lite-editor'

    def image_editor_url(self):
        path = reverse('image-editor', kwargs={'image_slug': 'test_simulated'})
        assert resolve(path).view_name == 'image-editor'

    def images_list_url(self):
        path = reverse('images_list')
        assert resolve(path).view_name == 'images_list'