# API Documentation

This document provides a detailed reference for all available API endpoints in the AI-Powered Quiz Application.

## 🔐 Authentication
The API uses JSON Web Tokens (JWT) for authentication.
- **Header**: `Authorization: Bearer <your_access_token>`
- **Token URL**: `/api/v1/auth/login/`

## 📂 Quizzes (`/api/v1/quizzes/`)

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | List all published quizzes or user's owned quizzes. | Anyone |
| `POST` | `/` | Create a new quiz (with optional AI generation). | Auth |
| `GET` | `/{id}/` | Get detailed information about a specific quiz. | Anyone |
| `PATCH` | `/{id}/` | Update an existing quiz. | Owner |
| `DELETE` | `/{id}/` | Delete a quiz. | Owner |
| `POST` | `/{id}/submit/` | Submit a draft quiz for admin review. | Owner |
| `POST` | `/{id}/publish/` | Publish a pending quiz. | Admin |
| `POST` | `/{id}/reject/` | Reject a pending quiz. | Admin |
| `GET` | `/pending/` | List all quizzes awaiting review. | Admin |
| `POST` | `/{id}/attempts/` | Start a new attempt for a quiz. | Auth |
| `POST` | `/{id}/rating/` | Rate and review a quiz (1-5). | Auth |

### AI Generation Request Body
```json
{
  "title": "Python Basics",
  "category": "uuid-here",
  "difficulty": "MEDIUM",
  "generate_with_ai": true,
  "num_questions": 5
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
| `POST` | `/start/{quiz_id}/` | Alternative way to start a quiz attempt. | Auth |
| `GET` | `/{id}/questions/` | Fetch questions for an active attempt (handles shuffling). | Auth |
| `POST` | `/{id}/answers/` | Submit an answer for a specific question. | Auth |
| `POST` | `/{id}/submit/` | Finish and grade the attempt. | Auth |
| `GET` | `/{id}/review/` | Review completed attempt with correct answers. | Auth |

## 👥 Interactions & Notifications

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/interactions/follows/` | Follow another user. | Auth |
| `GET` | `/api/v1/interactions/notifications/` | View your notifications. | Auth |
| `PATCH` | `/api/v1/interactions/notifications/{id}/` | Mark as read. | Auth |

## 📊 Analytics & Search

| Method | Endpoint | Description | Perms |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/search?q=query` | Global search across quizzes and tags. | Public |
| `GET` | `/api/v1/analytics/stats/` | General platform statistics. | Admin |

## 🚦 Throttling
- **Anonymous**: 100 requests per day.
- **Authenticated User**: 1,000 requests per day.

## 📄 Pagination
All list endpoints support pagination via `?page=N`. Default page size is 10.
