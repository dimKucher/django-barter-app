from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth import get_user_model
from app_ads.models import AdsItem
from app_ads.views import BaseAdsListView, AdsUpdate, AdsDelete
from app_ads import models, forms, views
from app_ads import services
from django.test.utils import override_settings
User = get_user_model()


class AdsViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.other_user = User.objects.create_user(username='otheruser', password='pass')

        self.ad1 = AdsItem.objects.create(title='Ad from user', user=self.user)
        self.ad2 = AdsItem.objects.create(title='Ad from other_user', user=self.other_user)

        self.item = AdsItem.objects.create(
            title="Test Ad",
            description="Description",
            category="ELECTRONICS",
            condition="NEW",
            user=self.user,
        )

        self.url_list = reverse('app_ads:list')
        self.url_list_user = reverse('app_ads:list_user')
        self.template = 'ads/ads_list.html'

    def login(self):
        self.client.login(username='testuser', password='pass')

    def test_ads_list_view_status_code(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)

    def test_ads_list_view_uses_correct_template(self):
        response = self.client.get(self.url_list)
        self.assertTemplateUsed(response, self.template)

    def test_ads_list_context_includes_extra_context(self):
        response = self.client.get(self.url_list)
        self.assertIn('empty_message', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('conditions', response.context)

    def test_ads_list_shows_ads_not_owned_by_user(self):
        self.login()
        response = self.client.get(self.url_list)
        ads = response.context['object_list']
        for ad in ads:
            self.assertNotEqual(ad.user, self.user)

    def test_ads_user_list_requires_login(self):
        response = self.client.get(self.url_list_user)
        self.assertEqual(response.status_code, 302)

    def test_ads_user_list_returns_user_ads(self):
        self.login()
        response = self.client.get(self.url_list_user)
        ads = response.context['object_list']
        for ad in ads:
            self.assertEqual(ad.user, self.user)

    def test_pagination_is_applied(self):
        for i in range(10):
            AdsItem.objects.create(title=f"Ad {i}", user=self.other_user)
        response = self.client.get(self.url_list)
        self.assertIn('page_obj', response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['object_list']), BaseAdsListView.paginate_by)

    def test_create_requires_login(self):
        response = self.client.get(reverse('app_ads:create'))
        self.assertEqual(response.status_code, 302)

    def test_create_success(self):
        self.login()
        response = self.client.post(reverse('app_ads:create'), {
            'title': 'New Ad',
            'description': 'Some description',
            'category': 'ELECTRONICS',
            'condition': 'NEW',
            'user': self.user
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(AdsItem.objects.filter(title='New Ad').exists())

    def test_detail_view(self):
        response = self.client.get(reverse('app_ads:detail', kwargs={'pk': self.item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/ads_detail.html')

    def test_update_not_owner_raises_permission_denied(self):
        factory = RequestFactory()
        request = factory.get(reverse('app_ads:update', kwargs={'pk': self.item.pk}))
        request.user = self.other_user

        view = AdsUpdate()
        view.kwargs = {'pk': self.item.pk}
        view.request = request

        with self.assertRaises(PermissionDenied):
            view.get_object()

    def test_update_success(self):
        self.login()
        response = self.client.post(reverse('app_ads:update', kwargs={'pk': self.item.pk}), {
            'title': 'Updated Title',
            'description': 'Updated description',
            'category': 'ELECTRONICS',
            'condition': 'NEW'
        }, follow=True)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, 'Updated Title')

    def test_delete_not_owner(self):
        factory = RequestFactory()
        request = factory.get(reverse('app_ads:delete', kwargs={'pk': self.item.pk}))
        request.user = self.other_user

        view = AdsDelete()
        view.kwargs = {'pk': self.item.pk}
        view.request = request

        with self.assertRaises(PermissionDenied):
            view.get_object()

    def test_delete_success(self):
        self.login()
        response = self.client.post(reverse('app_ads:delete', kwargs={'pk': self.item.pk}), follow=True)
        self.assertFalse(AdsItem.objects.filter(pk=self.item.pk).exists())
