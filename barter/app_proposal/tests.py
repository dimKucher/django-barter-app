from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from app_ads.models import AdsItem
from app_proposal.models import ExchangeProposal
from app_proposal import views


class ProposalBaseTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')
        self.other_user = User.objects.create_user(username='other', password='pass')

        self.ad_item = AdsItem.objects.create(
            title="Cellphone",
            description="Cellphone pro max",
            user=self.receiver,
            category="ELECTRONICS",
            condition="NEW"
        )
        self.ad_other_item = AdsItem.objects.create(
            title="Microwave",
            description="Microwave 2000W",
            user=self.receiver,
            category="ELECTRONICS",
            condition="NEW"
        )

        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.sender,
            ad_receiver=self.receiver,
            item=self.ad_item,
            status=ExchangeProposal.STATUS_PENDING
        )

    def test_proposal_list_view_authenticated(self):
        self.client.login(username='receiver', password='pass')
        response = self.client.get(reverse('app_proposal:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proposal/proposal_list.html')
        self.assertIn('sender_list', response.context)
        self.assertIn('status_list', response.context)

    def test_proposal_list_view_requires_login(self):
        response = self.client.get(reverse('app_proposal:list'))
        self.assertEqual(response.status_code, 302)

    def test_create_proposal_success(self):
        self.client.login(username='sender', password='pass')
        response = self.client.post(
            reverse('app_proposal:request', kwargs={'pk': self.ad_item.pk}),
            data={
                "ad_sender": self.sender,
                "ad_receiver": self.receiver,
                "item": self.ad_other_item.pk,
                "status": ExchangeProposal.STATUS_PENDING
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ExchangeProposal.objects.filter(ad_sender=self.sender, item=self.ad_item).exists())

    def test_create_proposal_self_request_forbidden(self):
        factory = RequestFactory()
        request = factory.get(reverse('app_proposal:request', kwargs={'pk': self.ad_item.pk}))
        request.user = self.receiver

        view = views.ProposalCreateView()
        view.request = request
        view.kwargs = {'pk': self.ad_item.pk}

        with self.assertRaises(PermissionDenied):
            view.get_object()

    def test_proposal_detail_authenticated(self):
        self.client.login(username='receiver', password='pass')
        response = self.client.get(reverse('app_proposal:detail', kwargs={'pk': self.proposal.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.proposal.item.title)

    def test_proposal_detail_requires_login(self):
        response = self.client.get(reverse('app_proposal:detail', kwargs={'pk': self.proposal.pk}))
        self.assertEqual(response.status_code, 302)

    def test_status_update_forbidden_if_not_receiver(self):
        self.client.login(username='sender', password='pass')
        response = self.client.get(reverse('app_proposal:accept', kwargs={'pk': self.proposal.pk}))
        self.assertContains(response, "Недостаточно прав доступа", status_code=200)

    def test_status_update_forbidden_if_not_pending(self):
        self.proposal.status = ExchangeProposal.STATUS_ACCEPTED
        response = self.client.get(reverse('app_proposal:accept', kwargs={'pk': self.proposal.pk}))
        self.assertContains(response, "Недостаточно прав доступа", status_code=200)

    def test_accept_proposal_success(self):
        self.client.login(username='receiver', password='pass')
        response = self.client.post(reverse('app_proposal:accept', kwargs={'pk': self.proposal.pk}), follow=True)
        self.proposal.refresh_from_db()
        self.ad_item.refresh_from_db()
        self.assertEqual(self.proposal.status, ExchangeProposal.STATUS_ACCEPTED)
        self.assertTrue(self.ad_item.is_given)

    def test_reject_proposal_success(self):
        self.client.login(username='receiver', password='pass')
        response = self.client.post(reverse('app_proposal:reject', kwargs={'pk': self.proposal.pk}), follow=True)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.status, ExchangeProposal.STATUS_REJECTED)

    def test_accept_proposal_rejects_others(self):
        other_proposal = ExchangeProposal.objects.create(
            ad_sender=self.other_user,
            ad_receiver=self.receiver,
            item=self.ad_item,
            status=ExchangeProposal.STATUS_PENDING
        )

        self.client.login(username='receiver', password='pass')
        self.client.post(reverse('app_proposal:accept', kwargs={'pk': self.proposal.pk}), follow=True)

        other_proposal.refresh_from_db()
        self.assertEqual(other_proposal.status, ExchangeProposal.STATUS_REJECTED)
