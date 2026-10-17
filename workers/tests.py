from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from residents.models import Payment, ResidentProfile
from workers.models import WorkerProfile


class ConfirmOfflinePaymentTests(TestCase):
    def setUp(self):
        worker_user = User.objects.create_user(
            username='worker',
            password='test-password',
        )
        self.worker = WorkerProfile.objects.create(
            user=worker_user,
            worker_id='WORKER-1',
        )
        resident_user = User.objects.create_user(
            username='resident',
            password='test-password',
        )
        self.resident = ResidentProfile.objects.create(
            user=resident_user,
            ward_number='1',
            household_id='HOUSEHOLD-1',
            address='1 Test Street',
        )
        self.payment = Payment.objects.create(
            resident=self.resident,
            amount='250.00',
            is_paid_online=False,
            receipt_number='CASH-001',
        )
        self.client.force_login(worker_user)

    def test_cash_payment_can_only_be_confirmed_once(self):
        url = reverse('confirm_offline_payment')

        first_response = self.client.post(url, {'payment_id': self.payment.pk}, follow=True)
        self.assertRedirects(first_response, url)
        self.assertContains(
            first_response,
            f'Confirmed cash payment of ₹{self.payment.amount}',
        )
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.worker_who_received_cash, self.worker)

        second_response = self.client.post(url, {'payment_id': self.payment.pk}, follow=True)
        self.assertRedirects(second_response, url)
        self.assertContains(second_response, 'This payment is already confirmed.')
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.worker_who_received_cash, self.worker)
