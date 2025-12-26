# Personal Portfolio & System

A modern, full-stack personal website built with Flask and Firebase. Features a portfolio homepage, blog, projects showcase, digital products, knowledge vault, and secure admin panel.

## Features

### Public Pages
- **Portfolio Home** - Hero section, featured projects, expertise showcase, stats
- **Writings** - Blog with markdown support, series, and tags
- **Projects** - Portfolio with live demos, GitHub links, tech stack
- **Products** - Digital products marketplace
- **Systems** - Public tools and utilities
- **Vault** - Knowledge base with categories and filtering
- **Arena** - Commentary and discourse
- **Metrics** - Public performance dashboard
- **Work** - Collaboration terms and contact

### Admin Panel
- **Secure Authentication** - Firebase Auth with email/password
- **Content Management** - Full CRUD operations for all content types
- **Dashboard** - Overview stats and quick actions
- **Modern UI** - Clean, responsive admin interface

## Tech Stack

**Backend**
- Flask 3.0
- Python 3.8+
- Firebase Admin SDK
- Firestore Database

**Frontend**
- Jinja2 Templates
- CSS3 (Purple gradient theme)
- Vanilla JavaScript
- Firebase Web SDK

**Infrastructure**
- Firebase Authentication
- Firebase Firestore
- Markdown rendering
- RESTful architecture

## Project Structure

```
personal-website/
├── app/
│   ├── __init__.py           # App factory
│   ├── models/               # Data models
│   │   ├── post.py
│   │   ├── product.py
│   │   ├── project.py
│   │   └── metric.py
│   ├── routes/               # Blueprints
│   │   ├── main.py
│   │   ├── writings.py
│   │   ├── products.py
│   │   ├── projects.py
│   │   ├── systems.py
│   │   ├── vault.py
│   │   ├── arena.py
│   │   ├── metrics.py
│   │   ├── work.py
│   │   └── admin.py
│   ├── templates/            # Jinja templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── admin/
│   │   ├── writings/
│   │   ├── projects/
│   │   └── ...
│   └── static/
│       └── css/
│           ├── style.css     # Main styles
│           └── admin.css     # Admin styles
├── config.py                 # Configuration
├── run.py                    # Application entry
├── requirements.txt          # Dependencies
└── .env                      # Environment variables
```

## Installation

### Prerequisites
- Python 3.8+
- Firebase project with Firestore enabled
- Firebase service account credentials

### Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd personal-website
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Firebase Setup**
   - Create a Firebase project at https://console.firebase.google.com
   - Enable Firestore Database
   - Enable Authentication (Email/Password)
   - Download service account key (Project Settings → Service Accounts)

5. **Environment Configuration**

Create `.env` file in project root:
```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
GOOGLE_APPLICATION_CREDENTIALS=/path/to/firebase-key.json
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
```

6. **Firebase Web Config**

Update `app/templates/admin/login.html` with your Firebase config:
```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

7. **Create Admin User**
   - Go to Firebase Console → Authentication → Users
   - Click "Add user"
   - Enter email and password for admin access

8. **Create static directories**
```bash
mkdir -p app/static/css app/static/js app/static/assets
```

## Running Locally

```bash
python run.py
```

Visit `http://localhost:5000`

Admin panel: `http://localhost:5000/admin/login`

## Firestore Collections

The app uses the following Firestore collections:

**writings**
```javascript
{
  title: string,
  content: string,      // Markdown
  date: string,         // ISO 8601
  tags: array,
  series: string|null,
  slug: string
}
```

**projects**
```javascript
{
  title: string,
  description: string,
  demo_url: string|null,
  github_url: string|null,
  tech_stack: array,
  status: string,       // 'active', 'archived', 'wip'
  slug: string
}
```

**products**
```javascript
{
  title: string,
  description: string,
  price: number,
  url: string|null,
  active: boolean,
  slug: string
}
```

**tools**
```javascript
{
  title: string,
  description: string,
  url: string|null,
  category: string
}
```

**vault**
```javascript
{
  title: string,
  content: string,      // Markdown
  category: string,
  tags: array
}
```

**arena**
```javascript
{
  title: string,
  content: string,      // Markdown
  date: string,
  tags: array
}
```

**metrics**
```javascript
{
  metric: string,
  value: number|string,
  unit: string,
  updated: string,      // ISO 8601
  category: string
}
```

## Deployment

### Production Setup

1. **Update environment**
```bash
FLASK_ENV=production
SECRET_KEY=<strong-random-key>
```

2. **Use JSON string for credentials** (recommended for cloud deployments)
```bash
FIREBASE_CREDENTIALS='{"type":"service_account",...}'
```

3. **Deploy to your platform**
   - Heroku: Use `Procfile`
   - Railway: Auto-detects Flask
   - Google Cloud Run: Use `Dockerfile`
   - AWS: Use Elastic Beanstalk or Lambda

### Example: Heroku

```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret
heroku config:set FIREBASE_CREDENTIALS='<json-string>'
git push heroku main
```

## Admin Panel Usage

1. **Login** at `/admin/login`
2. **Dashboard** shows content stats
3. **Manage Content**:
   - Add/Edit/Delete writings
   - Add/Edit/Delete projects
   - Add/Edit/Delete products
4. **Markdown Support** - Write content in markdown, rendered automatically

## Customization

### Styling
- Edit `app/static/css/style.css` for main site
- Edit `app/static/css/admin.css` for admin panel
- Colors defined in CSS variables at top of file

### Content
- Update `app/templates/home.html` for portfolio content
- Replace placeholder text with your information
- Update `app/templates/work.html` with contact details

### Features
- Add new routes in `app/routes/`
- Add new models in `app/models/`
- Create new templates in `app/templates/`

## Security Notes

- Never commit `.env` or Firebase credentials to git
- Use strong SECRET_KEY in production
- Firebase Auth handles password security
- Session cookies are httpOnly and sameSite
- Admin routes protected with `@login_required`

## License

MIT License - Feel free to use for your own portfolio

## Support

For issues or questions:
- Check Firebase Console for database errors
- Verify environment variables are set correctly
- Check Flask logs for debugging

---

Built with Flask, Firebase, and dedication to clean architecture.