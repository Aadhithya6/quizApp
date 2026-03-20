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

> [!TIP]
> **View Interactive Schema**: For a detailed view of all table attributes and relationships, check the [Interactive ERD Documentation](./ERD.html).Download this file from github and open in chrome browser.
### Core Relationships:
- **Users & Quizzes**: Users create quizzes (Owners). Admin/Moderators can review and publish them.
- **Quizzes & Questions**: A quiz is a collection of ordered questions.
- **Attempts**: Tracks a user's journey through a quiz, calculating the score upon completion.
- **Interactions**: Users can follow each other, rate quizzes, and receive notifications for key events.

## 🤖 AI Integration Approach

* **AI Service Layer**: I implemented AI integration using a dedicated service layer to keep external API calls isolated from core application logic.
* **Prompt Design**: The system sends structured prompts including topic, difficulty, and number of questions to generate consistent quiz content.
* **Structured JSON Output**: The AI is instructed to return responses in a strict JSON format, which is then parsed and validated before storing in the database.
* **Error Handling and Validation**: I implemented validation checks to handle incomplete or malformed AI responses, ensuring only valid questions are saved.
* **Transactional Safety**: Quiz, questions, and options are created within a database transaction to ensure atomicity — if any part fails, the entire operation is rolled back.
* **Mocking for Testing**: AI calls are mocked during testing to ensure deterministic results and avoid dependency on external services.
* **Extensibility**: The integration is designed to support multiple providers (e.g., OpenAI, NVIDIA models) with minimal changes.

## 🏗️ Design Decisions and Trade-offs

> [!NOTE]
> **Architecture Evolution**: For a detailed deep-dive into how the system's architecture evolved from a basic quiz to a production-ready attempt system, see [ARCHITECTURAL_DECISIONS.md](./ARCHITECTURAL_DECISIONS.md).

* **Separation of Quiz, Attempt, and Answer Models**: I separated Quiz (template), Attempt (user session), and Answer (per-question response) to ensure clean data modeling and support multiple attempts per user. This improves scalability and enables detailed analytics.
* **Use of Database Views for Analytics**: Instead of storing derived fields like average score and leaderboard rankings, I used database views. This avoids data redundancy and ensures consistency, at the cost of slightly higher query complexity.
* **Service Layer for Business Logic**: I moved complex logic such as AI generation, scoring, and publishing into service functions to keep views clean and improve testability and maintainability.
* **UUIDs for Primary Keys**: I used UUIDs instead of auto-increment integers to prevent ID enumeration and improve security, especially for public APIs.
* **Multiple Attempts Allowed**: I allowed users to attempt quizzes multiple times to support learning and competition. Leaderboards are calculated using the best attempt per user.
* **Caching for Performance**: Frequently accessed endpoints like quiz listings and leaderboards are cached to reduce database load and improve response times.
* **Minimal but Extensible API Design**: I focused on keeping the API clean and minimal while ensuring it can be extended with features like notifications, ratings, and background tasks.

## 🧪 Challenges Faced and Solutions

* **AI Response Parsing and Validation**: AI-generated responses were sometimes inconsistent or malformed. I solved this by enforcing strict JSON structure validation and handling errors gracefully before saving data.
* **Leaderboard Ranking Logic**: Initially, leaderboard ordering did not correctly handle tie cases. I fixed this by introducing a secondary sorting condition using `time_taken` as a tie-breaker.
* **Cache Interference in Testing**: Cached data caused inconsistent test results. I resolved this by clearing the cache in the test setup to ensure isolation between test cases.
* **Queryset Visibility for Draft Quizzes**: Users were unable to see their own draft or pending quizzes. I fixed this by refining queryset logic to include owner-specific visibility.
* **Handling Duplicate Answers**: Users could potentially submit multiple answers for the same question. I enforced uniqueness constraints and implemented idempotent updates to ensure data consistency.
* **UUID Handling in Tests**: Comparing UUIDs and strings caused issues in edge case tests. I resolved this by standardizing type handling across the application.

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
