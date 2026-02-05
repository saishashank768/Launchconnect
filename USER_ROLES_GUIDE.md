# LaunchConnect User Roles & Access Guide

## 4 User Types Overview

### 1. **Student** (role='student')
- **Purpose**: Find internships and job opportunities
- **Dashboard**: `/student-dashboard/`
- **Key Features**:
  - Browse verified job listings (job_list view)
  - Apply to jobs (creates Application record)
  - Track application status in real-time
  - Build professional profile (resume_url, skills, education, availability)
  - Actively Looking flag controls resume push to companies
  - Skill Match Score computed from matching job requirements
- **Models**: `StudentProfile`
- **Key Views**: 
  - `students.views.dashboard` - Main dashboard
  - `students.views.profile_edit` - Edit profile
  - `jobs.views.job_list` - Browse jobs
  - `jobs.views.job_detail` - View job details
  - `applications.views.apply_job` - Submit application

---

### 2. **Startup** (role='startup')
- **Purpose**: Post jobs and hire talent
- **Dashboard**: `/startup-dashboard/`
- **Key Features**:
  - Post and manage job listings
  - Review applicants for posted jobs
  - Email verification for company authenticity
  - Analytics: total applicants per job
  - Job status management (OPEN, CLOSED, etc.)
- **Models**: `StartupProfile`, `Job`, `Application`
- **Key Views**:
  - `startups.views.dashboard` - Main dashboard
  - `startups.views.job_create` - Post a new job
  - `startups.views.job_list` - View all posted jobs
  - `startups.views.applicants` - Review applicants
  - `startups.views.profile_edit` - Edit company profile

---

### 3. **Founder** (role='founder')
- **Purpose**: Private network for founders to collaborate and share needs
- **Feed**: `/founder-collab/`
- **Key Features**:
  - Post collaboration needs (hiring, advisors, investors, etc.)
  - Browse other founder's needs in the network
  - Send collaboration requests to other founders
  - Manage incoming collaboration requests
  - Collaboration score (reputation system)
  - Email domain verification (same as startup)
  - Notifications for new collab requests
- **Models**: `FounderNeed`, `CollabRequest`, `Notification`
- **Key Views**:
  - `founder_collab.views.feed` - Browse founder network
  - `founder_collab.views.post_need` - Post a collaboration need
  - `founder_collab.views.send_request` - Send collab request to founder
  - `founder_collab.views.manage_requests` - Manage incoming requests

---

### 4. **Admin** (role='admin')
- **Purpose**: Platform management and oversight
- **Dashboard**: `/admin-dashboard/`
- **Key Features**:
  - View platform statistics
  - Manage user accounts and roles
  - Monitor job postings and applications
  - Manage flagged content/abuse
- **Models**: Django Admin + Custom Admin views
- **Key Views**:
  - `admin_panel.views.admin_dashboard` - Admin overview
  - Django's built-in `/admin/` for superuser access

---

## Database Models by Role

| Model | Belongs To | Purpose |
|-------|-----------|---------|
| `StudentProfile` | Student | Stores student info: skills, resume, education, availability, actively_looking |
| `StartupProfile` | Startup | Stores company info: verification status, hire_score |
| `Job` | Startup | Job postings created by startups |
| `Application` | Student | Track student applications to jobs |
| `FounderNeed` | Founder | Founder collaboration needs |
| `CollabRequest` | Founder | Requests to collaborate with other founders |
| `Notification` | User | Notifications for all user types |

---

## URL Routing by Role

```python
# users/ - Auth & Home
GET  /                          → users.views.home (public landing page)
GET  /register/                 → users.views.register (choose role: student/startup/founder)
POST /register/                 → Create user with selected role
GET  /login/                    → auth.login
POST /login/                    → auth.login
GET  /logout/                   → auth.logout

# students/
GET  /student-dashboard/        → students.views.dashboard
GET  /student-profile/edit/     → students.views.profile_edit
POST /student-profile/edit/     → Save profile changes

# startups/
GET  /startup-dashboard/        → startups.views.dashboard
GET  /startup/jobs/new/         → startups.views.job_create
GET  /startup/jobs/             → startups.views.job_list
GET  /startup/applicants/       → startups.views.applicants
GET  /startup-profile/edit/     → startups.views.profile_edit

# jobs/ (public & both student/startup use)
GET  /jobs/                     → jobs.views.job_list
GET  /jobs/<id>/                → jobs.views.job_detail
POST /jobs/<id>/apply/          → applications.views.apply_job

# founder_collab/
GET  /founder-collab/           → founder_collab.views.feed
GET  /founder-collab/post/      → founder_collab.views.post_need
POST /founder-collab/post/      → Create FounderNeed
GET  /founder-collab/request/   → founder_collab.views.send_request
POST /founder-collab/request/   → Create CollabRequest
GET  /founder-collab/manage-requests/ → founder_collab.views.manage_requests
POST /founder-collab/manage-requests/ → Accept/Decline collab requests

# admin_panel/
GET  /admin-dashboard/          → admin_panel.views.admin_dashboard
```

---

## Authentication Flow

1. **User Registration**:
   - Visit `/register/`
   - Choose role: Student, Startup, or Founder
   - Create account → User record created with `role` field

2. **Role-Based Access Control**:
   - All views check `request.user.is_student()`, `is_startup()`, `is_founder()`, etc.
   - Redirect to login if user doesn't have required role
   - Example: `/founder-collab/` redirects to `/login/` if not a founder

3. **Profile Creation**:
   - Student: `StudentProfile` (resume, skills, education)
   - Startup: `StartupProfile` (company info, verification)
   - Founder: Can be a verified startup acting as founder

---

## Recent Fixes Applied

### Fix 1: Founder Feed View (`founder_collab/views.py`)
**Issue**: `feed()` view returned `None` instead of `HttpResponse`
**Solution**: Added missing `render()` call with context containing founder needs
```python
context = {
    'needs': needs,
    'is_verified': is_verified,
}
return render(request, 'founder_collab/founder_feed.html', context)
```

### Fix 2: Student Dashboard (`students/views.py`)
**Added**: Dynamic skill match score based on open jobs
**Context Variables**:
- `profile` - StudentProfile instance
- `applications` - Student's applications
- `recommended_jobs` - AI-matched job recommendations
- `skill_match_score` - % of student's skills found in open jobs (0-100)

### Fix 3: Homepage UI (`users/templates/users/home.html`)
**Updated**: Full landing page with hero, choose-path cards, features, testimonials, CTA

---

## Testing Each Role

### Test Student:
1. Register as "Student"
2. Visit `/student-dashboard/` → Should see applications & skill match
3. Visit `/jobs/` → Should see job list
4. Click "Apply" on a job → Should create Application

### Test Startup:
1. Register as "Startup"
2. Visit `/startup-dashboard/` → Should see posted jobs
3. Click "Post Job" → Create a new Job posting
4. Should verify company via email domain before posting

### Test Founder:
1. Register as "Founder"  
2. Visit `/founder-collab/` → Should see founder network feed
3. Click "Post a Need" → Create FounderNeed (hiring, advisor, etc.)
4. Browse other founder needs → Can send collaboration requests

### Test Admin:
1. Register as "Admin" (or use Django admin)
2. Visit `/admin-dashboard/` → View platform stats

---

## Key Features by Role

| Feature | Student | Startup | Founder | Admin |
|---------|---------|---------|---------|-------|
| Browse Jobs | ✅ | ✅ | - | - |
| Apply to Jobs | ✅ | - | - | - |
| Post Jobs | - | ✅ | - | - |
| Review Applicants | - | ✅ | - | - |
| Collaboration Network | - | - | ✅ | - |
| Post Needs | - | - | ✅ | - |
| Platform Management | - | - | - | ✅ |
| Verification Required | - | ✅ | ✅ | - |

---

## Next Steps

To ensure everything works smoothly:

1. **Run migrations** (if not done):
   ```bash
   python manage.py makemigrations students
   python manage.py migrate
   ```

2. **Test each role** using the URLs above

3. **Check email verification** for Startup & Founder roles

4. **Verify role-based redirects** are working (e.g., student accessing founder feed should redirect)
