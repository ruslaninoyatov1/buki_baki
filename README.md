# Kids Education Portal

Kids educational web portal with CMS system for content management through admin panel.

## Key Features

- **Video Lessons** - Educational videos for kids
- **Coloring Pages** - Coloring files in PDF/PNG format
- **Tasks** - Educational assignments and exercises
- **Subscription** - Subscription system with Basic and Popular plans
- **Categories** - Content organization by categories
- **Multilingual** - Support for Russian and English languages

## Tech Stack

- **Backend**: Django (Python 3.8+)
- **Database**: MySQL (production)
- **Authentication**: Django sessions with 360-day expiration

## Installation and Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd kids_education_portal
   ```

2. Create virtual environment:
   ```
   python -m venv venv
   ```

3. Activate virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Configure database settings in `kids_education_portal/settings.py`:
   ```
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'buki-baki-baza',
           'USER': 'buki-baki-admin',
           'PASSWORD': '$%>K|RM;&-Ye^lV$',
           'HOST': '178.254.23.217',
           'PORT': '3306',
       }
   }
   ```

6. Apply migrations:
   ```
   python manage.py migrate
   ```

7. Create superuser:
   ```
   python manage.py createsuperuser
   ```

8. Run development server:
   ```
   python manage.py runserver
   ```

## Admin Panel Access

- URL: http://127.0.0.1:8000/panel/
- Use superuser credentials created in step 7

## Project Structure

```
kids_education_portal/
├── ads/              # Advertising blocks
├── api/              # REST API endpoints
├── banners/          # Website banners
├── categories/       # Content categories
├── coloring/         # Coloring pages
├── contacts/         # Contact form
├── feedback/         # Feedback system
├── profile_app/      # User profile
├── subscription/     # Subscription system
├── tasks/            # Educational tasks
├── video/            # Educational videos
├── manage.py         # Django management utility
└── requirements.txt  # Project dependencies
```

## API Endpoints

All frontend templates and static assets have been removed. The project now functions as a pure backend API:

- **Mobile API**: `/mobile/` - Mobile application endpoints
- **Video API**: `/videos/` - Video content endpoints
- **Coloring API**: `/coloring/` - Coloring content endpoints
- **Tasks API**: `/tasks/` - Educational tasks endpoints
- **Profile API**: `/profile/` - User profile endpoints
- **Contacts API**: `/contacts/` - Contact form endpoint

## License

This project is proprietary to the client and must not be distributed without permission.