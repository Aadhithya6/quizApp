# API Documentation

This document provides a detailed reference for all available API endpoints in the AI-Powered Quiz Application.

## 🔐 Authentication
The API uses JSON Web Tokens (JWT) for authentication.
- **Header**: `Authorization: Bearer <your_access_token>`
- **Token URL**: `/api/v1/auth/login/`
- **Refresh URL**: `/api/v1/auth/refresh/`

## 🛡️ Permissions & Roles

- **Public**: Anyone can access.
- **Authenticated**: Requires a valid JWT token.
- **Admin**: Staff users only.
- **Owner**: The user who created the quiz (`Quiz.created_by`).

## 👤 User Data (`/api/v1/users/me/`)

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Get current user profile. | Authenticated |
| `GET` | `/attempts/` | Get user's quiz attempt history. | Authenticated |
| `GET` | `/quizzes/` | Get quizzes created by the user. | Authenticated |

### 📋 User Profile Example
```json
{
  "id": "u1-v2-w3",
  "username": "johndoe",
  "email": "john@example.com",
  "role": "USER",
  "avatar_url": null
}
```

## 📂 Quizzes (`/api/v1/quizzes/`)

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | List all published quizzes or user's owned quizzes. | Public |
| `POST` | `/` | Create a new quiz (with optional AI generation). | Authenticated |
| `GET` | `/{id}/` | Get detailed information about a specific quiz. | Public |
| `PATCH` | `/{id}/` | Update an existing quiz. | Owner |
| `DELETE` | `/{id}/` | Delete a quiz. | Owner |
| `POST` | `/{id}/submit/` | Submit a draft quiz for admin review. | Owner |
| `POST` | `/{id}/publish/` | Publish a pending quiz. | Admin |
| `POST` | `/{id}/reject/` | Reject a pending quiz. | Admin |
| `GET` | `/pending/` | List all quizzes awaiting review. | Admin |
| `POST` | `/{id}/attempts/` | Start a new attempt for a quiz. | Authenticated |
| `POST` | `/{id}/retry/` | Shorthand to start a new attempt (increments attempt_number). | Authenticated |
| `POST` | `/{id}/rating/` | Rate and review a quiz (1-5). | Authenticated |
| `GET` | `/{id}/ratings/` | List all ratings for a quiz (includes avatars). | Public |
| `GET` | `/{id}/attempts/` | List your attempts for this quiz (Admin sees all). | Authenticated |

### 📋 Quiz Response Example
```json
{
  "id": "e4b3c2a1-5d6e-7f8a-9b0c-1d2e3f4g5h6i",
  "title": "Python Basics",
  "topic": "Programming",
  "difficulty": "MEDIUM",
  "category_name": "Computer Science",
  "question_count": 10,
  "created_at": "2024-03-20T10:00:00Z"
}
```

## 📝 Questions & Options

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/questions/` | List questions for a quiz. | Public |
| `POST` | `/api/v1/questions/` | Add a question manually. | Owner |
| `PATCH` | `/api/v1/questions/{id}/` | Edit a question. | Owner |
| `PATCH` | `/api/v1/options/{id}/` | Edit an option. | Owner |

## 🕹️ Quiz Attempts (`/api/v1/attempts/`)

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `GET` | `/{id}/questions/` | Fetch questions for an active attempt (handles shuffling). | Authenticated |
| `POST` | `/{id}/answers/` | Submit an answer for a specific question. | Authenticated |
| `POST` | `/{id}/submit/` | Finish and grade the attempt. | Authenticated |

### 📋 Answer Submission Example

**Endpoint**: `POST /api/v1/attempts/{id}/answers/`

**Request Body**:
```json
{
  "question": "550e8400-e29b-41d4-a716-446655440000",
  "selected_option": "660f9511-f30c-52e5-b827-557766551111",
  "is_skipped": false
}
```

**Field Explanations**:
- `question` (UUID): The ID of the question being answered.
- `selected_option` (UUID): The ID of the chosen option (required if `is_skipped` is `false`).
- `is_skipped` (Boolean): Set to `true` to skip the question.

**Validation Rules**:
- The question must belong to the quiz associated with the attempt.
- The selected option must belong to the specified question.
- You cannot answer the same question multiple times in a single attempt.
| `GET` | `/{id}/review/` | Review completed attempt with correct answers. | Authenticated |

### 📋 Attempt Response Example
```json
{
  "id": "uuid-attempt-123",
  "quiz_title": "Python Basics",
  "status": "COMPLETED",
  "score": 85.0,
  "started_at": "2024-03-20T10:05:00Z",
  "completed_at": "2024-03-20T10:15:00Z",
  "time_taken": 600
}
```

## 👥 Interactions & Notifications

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/interactions/follows/` | Follow another user. | Authenticated |
| `GET` | `/api/v1/interactions/notifications/` | View your notifications. | Authenticated |
| `PATCH` | `/api/v1/interactions/notifications/{id}/` | Mark as read. | Authenticated |
| `PATCH` | `/api/v1/interactions/notifications/read-all/` | Mark all as read. | Authenticated |

## 🏥 Health Check

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health/` | API health status. | Public |

## 📊 Analytics & Search

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/search?q=query` | Global search across quizzes and tags. | Public |
| `GET` | `/api/v1/analytics/quizzes/{id}/stats/` | Detailed statistics for a specific quiz. | Public |
| `GET` | `/api/v1/analytics/quizzes/{id}/leaderboard/` | Top scores for a specific quiz. | Public |

### 📊 Stats Example
```json
{
  "quiz_id": "uuid",
  "total_attempts": 150,
  "average_score": 72.5,
  "pass_rate": 65.0,
  "average_rating": 4.5
}
```

### 🏆 Leaderboard Example
```json
[
  {
    "user__username": "quizmaster",
    "best_score": 100.0,
    "min_time": 45,
    "total_attempts": 1
  },
  {
    "user__username": "python_pro",
    "best_score": 95.0,
    "min_time": 60,
    "total_attempts": 2
  }
]
```

## ❗ Error Format

When an error occurs, the API returns a standard error response:

```json
{
  "error": "ValidationError",
  "message": "Invalid input provided.",
  "details": {
    "field_name": ["This field is required."]
  }
}
```

## 🚦 Throttling
- **Anonymous**: 100 requests per day.
- **Authenticated User**: 1,000 requests per day.

## 📄 Pagination
All list endpoints support pagination via `?page=N`. Default page size is 10.
