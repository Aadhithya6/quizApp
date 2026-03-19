# AI-Powered Quiz Application API

Production-grade Django REST API for an AI-powered Quiz Application.

## 🚀 Features
- **Clean Architecture**: Modular apps, service layer, and serializers.
- **Strict Schema**: UUID PKs, proper indexing, and relational integrity.
- **JWT Auth**: Secure authentication and role-based access control.
- **Quiz Flow**: Drafting, submission for review, and publishing.
- **Attempt System**: Shuffling, point calculation, and attempt tracking.
- **Analytics**: Leaderboards and quiz statistics.

## 🛠️ Tech Stack
- Django & DRF
- PostgreSQL (Database)
- SimpleJWT (Auth)
- Redis (Optional, not implemented in this version)

## 📋 Run Instructions

### 1. Setup Environment
```bash
# Clone the repository
git clone <repo-url>
cd quizApp

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Database
Create a `.env` file based on `.env.example` and provide your PostgreSQL credentials.

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 5. Start Development Server
```bash
python manage.py runserver
```

### 6. Access API Documentation
Open `http://localhost:8000/api/v1/` to explore the endpoints.

## 📁 Project Structure
- `accounts`: User & Authentication
- `quizzes`: Categories, Tags, and Quiz metadata
- `questions`: Question & Option management
- `attempts`: Quiz attempt logic & scoring
- `interactions`: Ratings, Follows, and Notifications
- `analytics`: Stats & Leaderboards
- `common`: Utilities, permissions, and shared views
- `quiz_app`: Project configuration & settings
