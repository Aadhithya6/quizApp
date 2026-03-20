# API Documentation

This document provides a detailed reference for all available API endpoints in the AI-Powered Quiz Application.

## 🔐 Authentication
The API uses JSON Web Tokens (JWT) for authentication.
- **Header**: `Authorization: Bearer <your_access_token>`
- **Login**: `POST /api/v1/auth/login/`
- **Refresh**: `POST /api/v1/auth/refresh/`

### 📋 Token Refresh Example
**Request Body**:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## 🛡️ Permissions & Roles

- **Public**: Anyone can access (Read-only).
- **Authenticated**: Requires a valid JWT token.
- **Admin**: Staff users only (Manage Categories/Tags, Review Quizzes).
- **Owner**: The user who created the resource (`created_by`).

---

## 👤 User Profile (`/api/v1/users/me/`)

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Get current user profile. | Authenticated |
| `PATCH` | `/` | Update profile (bio, avatar, etc.). | Authenticated |
| `GET` | `/quizzes/` | Get quizzes created by you. | Authenticated |
| `GET` | `/attempts/` | Get your quiz attempt history. | Authenticated |

---

## 📂 Quizzes & Content

### 🏗️ Quizzes (`/api/v1/quizzes/`)

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | List all published quizzes. Supports filtering. | Public |
| `POST` | `/` | Create a new quiz (Manual or AI-generated). | Authenticated |
| `GET` | `/{id}/` | Get detailed quiz information. | Public |
| `PATCH` | `/{id}/` | Update quiz details. | Owner |
| `DELETE` | `/{id}/` | Delete a quiz. | Owner |
| `POST` | `/{id}/submit/` | Submit a draft for admin review. | Owner |
| `POST` | `/{id}/publish/` | Approve and publish a quiz. | Admin |
| `POST` | `/{id}/reject/` | Reject a pending quiz. | Admin |
| `GET` | `/pending/` | List quizzes awaiting review. | Admin |
| `POST` | `/{id}/attempts/` | Start a new attempt. | Authenticated |
| `POST` | `/{id}/retry/` | Shorthand to start a new attempt. | Authenticated |
| `POST` | `/{id}/rating/` | Submit/Update a rating (1-5). | Authenticated |
| `GET` | `/{id}/ratings/` | List all ratings for this quiz. | Public |

**Quiz Creation Example (AI)**:
`POST /api/v1/quizzes/`
```json
{
  "title": "History of Rome",
  "topic": "Roman Empire",
  "difficulty": "HARD",
  "generate_with_ai": true,
  "num_questions": 5
}
```

### 🏷️ Categories & Tags

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/categories/` | List all active categories. | Public |
| `POST` | `/api/v1/categories/` | Create a new category. | Admin |
| `GET` | `/api/v1/tags/` | List all active tags. | Public |
| `POST` | `/api/v1/tags/` | Create a new tag. | Admin |

### 📝 Questions & Options

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/questions/` | List all questions (filtered by quiz). | Public |
| `POST` | `/api/v1/questions/` | Create a question manually. | Owner |
| `GET` | `/api/v1/options/` | List options. | Public |
| `POST` | `/api/v1/options/` | Create an option. | Owner |

---

## 🕹️ Quiz Attempts (`/api/v1/attempts/`)

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `GET` | `/{id}/` | Get attempt summary and result. | Authenticated |
| `GET` | `/{id}/questions/` | Fetch questions for active attempt. | Authenticated |
| `POST` | `/{id}/answers/` | Submit/Update an answer. | Authenticated |
| `POST` | `/{id}/submit/` | Finish and grade the attempt. | Authenticated |
| `GET` | `/{id}/review/` | Detailed review with correct answers. | Authenticated |

**Answer Submission Example**:
`POST /api/v1/attempts/{id}/answers/`
```json
{
  "question": "uuid-question-id",
  "selected_option": "uuid-option-id",
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

## 👥 Interactions & Social

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/interactions/follows/` | Follow a user (`{"following": "user_id"}`). | Authenticated |
| `GET` | `/api/v1/interactions/notifications/` | List your notifications. | Authenticated |
| `PATCH` | `/api/v1/interactions/notifications/{id}/read/` | Mark as read. | Authenticated |
| `PATCH` | `/api/v1/interactions/notifications/read_all/` | Mark all as read. | Authenticated |

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

### 📄 Pagination
All list endpoints support `?page=N`. Default size is 10 items per page.

### ⚠️ Common Errors
- `401 Unauthorized`: Token missing or expired.
- `403 Forbidden`: Insufficient permissions (staff/owner required).
- `400 Bad Request`: Validation failure (e.g., attempt already finished).
