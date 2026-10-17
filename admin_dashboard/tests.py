from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from workers.models import CollectionAssignment, HKSWardAssignment, WorkerProfile


class AdminDashboardTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='test-password',
        )

    def test_admin_page_requires_superuser(self):
        regular_user = User.objects.create_user(
            username='regular',
            password='test-password',
        )
        self.client.force_login(regular_user)

        response = self.client.get(reverse('admin_monitoring_dashboard'))

        self.assertRedirects(
            response,
            f"{reverse('admin_login')}?next={reverse('admin_monitoring_dashboard')}",
        )

        self.client.force_login(self.admin)
        response = self.client.get(reverse('admin_monitoring_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_generate_monthly_schedule_creates_two_worker_assignments_once(self):
        worker1_user = User.objects.create_user(
            username='worker1',
            password='test-password',
        )
        worker2_user = User.objects.create_user(
            username='worker2',
            password='test-password',
        )
        worker1 = WorkerProfile.objects.create(user=worker1_user, worker_id='WORKER-1')
        worker2 = WorkerProfile.objects.create(user=worker2_user, worker_id='WORKER-2')
        HKSWardAssignment.objects.create(
            ward_id='WARD-01',
            worker1=worker1,
            worker2=worker2,
        )
        self.client.force_login(self.admin)
        url = reverse('generate_monthly_schedule')
        data = {'ward_id': 'WARD-01', 'month': 6, 'year': 2025}

        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('admin_monitoring_dashboard'))
        assignments = CollectionAssignment.objects.all()
        self.assertEqual(assignments.count(), 500)
        self.assertEqual(assignments.filter(worker=worker1).count(), 250)
        self.assertEqual(assignments.filter(worker=worker2).count(), 250)

        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('admin_monitoring_dashboard'))
        self.assertEqual(CollectionAssignment.objects.count(), 500)

    def test_monthly_report_loads_and_post_redirects_to_selected_period(self):
        self.client.force_login(self.admin)
        url = reverse('monthly_report')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Monthly Performance Report')

        response = self.client.post(url, {'month': 2, 'year': 2025})

        self.assertRedirects(response, f'{url}?month=2&year=2025')
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'February 2025')
