# AI-Powered Quiz Application API

Production-grade Django REST API for an AI-powered Quiz Application.

## 🚀 Features
- **AI-Powered Question Generation**: Automatically generate high-quality quiz questions using OpenAI or NVIDIA models.
- **Robust Attempt System**: Track user attempts, calculate scores, handle shuffling, and manage time limits.
- **Social & Engagement**: Quiz ratings (with user avatars), user follows, and a notification system (mark all as read).
- **Advanced Search & Filtering**: Global search across quizzes and fine-grained filtering by category, difficulty, or tags (active only).
- **Detailed Analytics**: Leaderboards, quiz stats, and attempt summaries.
- **Developer Friendly**: Health check endpoint and comprehensive API documentation.

## 🛠️ Tech Stack
- **Backend**: Django & Django REST Framework (DRF)
- **Database**: PostgreSQL (with UUID primary keys for security and scalability)
- **Authentication**: SimpleJWT (Access/Refresh token rotation)
- **AI Integration**: OpenAI SDK (compatible with NVIDIA NIM endpoints)
- **Caching**: Local memory cache (extensible to Redis)

## 📋 Local Setup

### 1. Prerequisites
- Python 3.10+
- PostgreSQL
- Git

### 2. Installation
```bash
# Clone the repository
git clone <repo-url>
cd quizApp

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/quiz_db
ALLOWED_HOSTS=localhost,127.0.0.1
OPENAI_API_KEY=your-api-key
NVIDIA_MODEL=meta/llama-3.1-405b-instruct  # Optional
```

### 4. Database Initialization
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Running the App
```bash
python manage.py runserver
```

## 📊 Database Schema

```mermaid
erDiagram
    USER ||--o{ QUIZ : created_by
    USER ||--o{ ATTEMPT : user
    USER ||--o{ QUIZ_RATING : user
    USER ||--o{ NOTIFICATION : user
    USER ||--o{ FOLLOW : follower
    USER ||--o{ FOLLOW : following
    
    CATEGORY ||--o{ QUIZ : category
    QUIZ ||--o{ QUESTION : quiz
    QUIZ ||--o{ ATTEMPT : quiz
    QUIZ ||--o{ QUIZ_TAG : quiz
    QUIZ ||--o{ QUIZ_RATING : quiz
    TAG ||--o{ QUIZ_TAG : tag
    
    QUESTION ||--o{ OPTION : question
    QUESTION ||--o{ ANSWER : question
    OPTION ||--o{ ANSWER : selected_option
    ATTEMPT ||--o{ ANSWER : attempt
```

### Core Relationships:
- **Users & Quizzes**: Users create quizzes (Owners). Admin/Moderators can review and publish them.
- **Quizzes & Questions**: A quiz is a collection of ordered questions.
- **Attempts**: Tracks a user's journey through a quiz, calculating the score upon completion.
- **Interactions**: Users can follow each other, rate quizzes, and receive notifications for key events.

## 🤖 AI Integration
The application uses AI to automate the creation of quiz content.
- **Workflow**: When creating a quiz, setting `generate_with_ai=True` triggers a service that calls the LLM.
- **Prompting**: The system passes the topic and difficulty to the AI, requesting a structured JSON response.
- **Data Integrity**: AI-generated JSON is parsed and validated before being converted into `Question` and `Option` records using a database transaction to ensure atomicity.

## 🏗️ Design Decisions
- **Service Layer**: Complex logic (like quiz publishing or attempt scoring) is extracted into service functions to keep views clean and testable.
- **UUIDs**: Used for all public-facing IDs to prevent enumeration attacks and simplify future database partitioning.
- **Permissions**: Access is controlled via roles (Public, Authenticated, Admin) and ownership. **Owner** is defined as the user who created the quiz (`Quiz.created_by`).
- **Throttling**: Implemented rate limiting (100/day for anon, 1000/day for users) to protect AI and database resources.
- **Caching Strategy**: Frequently accessed endpoints such as quiz listings and leaderboards are cached to improve performance and reduce database load.

## 🧪 Testing Approach
Comprehensive testing ensures reliability across the entire quiz lifecycle.
- **Tools**: Django's `APITestCase` with `unittest.mock` for AI services.
- **Coverage**:
    - **Auth**: Login and registration flows.
    - **Quiz Lifecycle**: Drafting -> Submission -> Admin Review -> Publishing.
    - **Attempts**: Starting, answering, and scoring logic.
    - **Edge Cases**: Unauthenticated access, invalid answers, and role-based permission violations.
- **Run Tests**:
  ```bash
  python manage.py test tests
  ```

## 🛠️ API Overview
The API is versioned at `v1`.
- **Auth**: `/api/v1/auth/` (Login, Register, Token Refresh)
- **Quizzes**: `/api/v1/quizzes/` (Manage and browse quizzes)
- **Questions**: `/api/v1/questions/` (Manage specific questions)
- **Attempts**: `/api/v1/attempts/` (Start and finish quiz attempts)
- **Analytics**: `/api/v1/analytics/` (Stats and leaderboards)

*For a full list of endpoints, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md).*
