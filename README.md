# Haritha Connect

A Django application for coordinating household waste collection among residents, Haritha Karma Sena workers, and administrators.

## Features

- **Resident portal:** View a resident dashboard, submit bin-full alerts with photo proof, report offline fee payments with receipt details/photo, submit complaints, request no collection for the current month, and view activity history.
- **Worker portal:** View daily collection assignments and assigned bin-full alerts, mark collections complete with photo proof, clear alerts, confirm reported cash payments, submit field issues, and view history.
- **Admin portal:** View monitoring counts, manage priority alerts and complaints, manage ward teams, generate monthly schedules, create one-off cover tasks, view overdue/unconfirmed payment lists, and view a monthly performance report.

## How it works

- **Monthly schedule generation:** For a selected ward, the generator creates 500 placeholder household assignments across 10 days starting on the fifth of the selected month: 50 tasks per day. With two assigned workers, the daily workload is split 25 tasks each; with one worker, that worker receives all 50. Existing assignments with the same date and household ID are ignored.
- **Bin-full alerts:** Residents can submit an alert with a photo. Administrators can assign an alert to a worker or mark it cleared; workers can clear alerts assigned to them.
- **Fee payment:** Residents can report an offline payment and attach receipt details/photo. The worker portal supports worker confirmation of reported cash payments. The project does not implement an online payment gateway.
- **Complaints:** Residents submit complaints and workers submit field issues. Administrators can update complaint status and add resolution notes to resident complaints.
- **Admin monitoring and monthly report:** The dashboard shows counts for pending alerts, complaints, unconfirmed cash payments, overdue bills, and collection progress for today. The monthly report summarizes assignments, completions, revenue records, resident complaints, and worker issues for a selected month.

## Tech stack

- Python
- Django
- SQLite
- Django templates, HTML, CSS, and JavaScript
- Pillow for Django image fields
- django-extensions (listed in the project settings)

## Roles and access control

- Resident, worker, and admin login pages are public.
- Worker operations require an authenticated account with a `WorkerProfile`.
- Admin dashboard pages require an authenticated superuser.
- Resident pages require authentication; resident actions that access resident data check for a `ResidentProfile`. Some views handle a missing profile with an access message or fallback response.
- Django's built-in admin site uses Django's staff/superuser permissions.

## Run it locally

Run these commands from the repository root in Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SECRET_KEY = (python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The environment variable applies to the current PowerShell session. If it is not set, development settings generate an ephemeral secret key when Django starts. Set a stable secret key through the deployment environment outside local development.

## Run the tests

```powershell
python manage.py test
```

## Limitations

- The admin alert buttons only flag follow-up and send no notification.
- The “assign daily task” screen creates placeholder cover tasks, not tasks mapped to actual households.
- Any worker can confirm any cash payment; confirmations are not restricted to a worker's ward.
- The project runs on SQLite with `DEBUG=True`; this configuration is for development, not production.
- The monthly generator uses a fixed 500-household count per ward rather than ward-specific household data.

## Author

Sreethika R
