
import os
import django
from django.conf import settings
from django.template.loader import get_template

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'launchconnect.settings')
django.setup()

templates_to_check = [
    'base.html',
    'error.html',
    'form_generic.html',
    'users/login.html',
    'users/register.html',
    'users/home.html',
    'students/student_dashboard.html',
    'startups/startup_dashboard.html',
    'jobs/job_list_v2.html',
    'jobs/job_detail.html',
    'founder_collab/founder_feed.html',
    'admin_panel/admin_dashboard.html'
]


with open('verification_result.txt', 'w') as f:
    f.write("Verifying template loading...\n")
    failed = []
    for t in templates_to_check:
        try:
            get_template(t)
            f.write(f"[OK] {t}\n")
        except Exception as e:
            f.write(f"[FAIL] {t}: {e}\n")
            failed.append(t)

    if failed:
        f.write(f"\nFailed to load {len(failed)} templates.\n")
    else:
        f.write("\nAll templates loaded successfully.\n")

if failed:
    exit(1)
else:
    exit(0)
