from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from datetime import date

from residents.models import BillingDue, NoCollectionRequest, ResidentProfile


class ResidentModelConstraintTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='resident',
            password='test-password',
        )
        self.resident = ResidentProfile.objects.create(
            user=user,
            ward_number='1',
            household_id='HOUSEHOLD-1',
            address='1 Test Street',
        )

    def test_billing_due_rejects_duplicate_resident_and_billed_date(self):
        BillingDue.objects.create(
            resident=self.resident,
            amount_due='250.00',
            billed_date=date(2025, 6, 1),
            due_date=date(2025, 6, 30),
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                BillingDue.objects.create(
                    resident=self.resident,
                    amount_due='300.00',
                    billed_date=date(2025, 6, 1),
                    due_date=date(2025, 6, 30),
                )

    def test_no_collection_request_rejects_duplicate_month_and_year(self):
        NoCollectionRequest.objects.create(
            resident=self.resident,
            collection_month=6,
            collection_year=2025,
            reason='LOW',
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                NoCollectionRequest.objects.create(
                    resident=self.resident,
                    collection_month=6,
                    collection_year=2025,
                    reason='VACATION',
                )
