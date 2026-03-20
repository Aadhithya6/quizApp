# Architectural Decisions & Design Evolution

This document outlines the iterative process and key design decisions made during the development of the AI-Powered Quiz Application.

---

### 1. Starting Point: Basic Quiz System
Initially, the design consisted of:
* **User**
* **Quiz**
* **Question**

While sufficient for a static system, it lacked the structure needed for real-world requirements like user attempts, scoring, and analytics.

---

### 2. Introducing Attempts for User Interaction
To support quiz participation, the **Attempt** model was introduced.
- **Why?** A quiz is a template; each user interaction must be tracked separately.
- **Benefits**: Enabled tracking user progress, supporting retries, and building leaderboard logic.

---

### 3. Adding Answer Model for Granular Tracking
The **Answer** model was separated from the **Attempt** model.
- **Why?** Each attempt contains multiple responses. Separation allows for per-question analytics, review functionality, and better normalization.
- **Constraint**: Enforced a uniqueness constraint on `(attempt_id, question_id)` to prevent duplicate submissions within a single attempt.

---

### 4. Normalizing Questions and Options
Separated **Question** and **Option** models.
- **Why?** Supports multiple options per question and provides flexibility for future question types (e.g., multi-select). Correct answers are stored in the `Option` model to avoid redundancy in the `Answer` model.

---

### 5. Supporting Categorization and Discoverability
Introduced **Category** (hierarchical) and **Tag** (many-to-many via `QuizTag`).
- **Why?** Categories provide broad classification (e.g., Programming), while tags allow for fine-grained filtering (e.g., Python, Django).

---

### 6. Adding Quiz Lifecycle (Moderation System)
Introduced `Quiz.status` (`DRAFT` → `PENDING` → `PUBLISHED` → `ARCHIVED`).
- **Why?** To ensure content quality through admin moderation. Users create drafts, submit for review, and admins control the publishing flow.

---

### 7. Designing Attempt Logic for Real-World Use
The **Attempt** model evolved to include:
- `attempt_number`: Tracks retries.
- `status`: `IN_PROGRESS` / `COMPLETED` / `AUTO_SUBMITTED`.
- `time_taken`: Used as a leaderboard tie-breaker.
- `is_passed`: Calculated based on the quiz's `passing_score`.

---

### 8. Avoiding Redundant Data (Analytics via Views)
Instead of storing aggregate fields like `total_attempts` or `average_score` in the models, the system uses **Database Views**.
- **Why?** Ensures real-time accuracy and avoids data inconsistency. Potential performance overhead is mitigated using a focused caching strategy.

---

### 9. AI Integration Design
AI-generated quizzes are handled via a dedicated service layer.
- **Decisions**: Enforce strict JSON structure validation and use database transactions to ensure that either the entire quiz (with its questions and options) is saved correctly, or nothing is saved at all.

---

### 10. Adding Social Features for Engagement
Introduced **QuizRating**, **Follow**, and **Notification** models.
- **Why?** To build a community around the quizzes, encourage repeat usage, and keep users engaged via automated notifications.

---

### 11. Security and Scalability Considerations
- **UUIDs**: Used for all public IDs to prevent enumeration attacks.
- **Throttling**: Rate limiting protects expensive AI endpoints and database resources.
- **Caching**: Improves performance for read-heavy operations like quiz listings and leaderboards.

---

### 12. Testing-Driven Refinements
Testing identified critical areas for improvement:
- **Cache Isolation**: Solved interference by clearing cache in test setups.
- **Leaderboard Logic**: Fixed tie-breaking using `time_taken`.
- **Visibility**: Refined querysets so users can see their own drafts while public users only see published content.

---

### 13. Final Architecture Summary
The final architecture prioritizes:
- **Separation of Concerns**: Quiz (template) vs. Attempt (session).
- **Scalability**: Normalized schema with efficient relationships.
- **Reliability**: Robust validation, transactional safety, and comprehensive testing.

The design evolved from a simple model into a production-ready system by iteratively addressing real-world requirements for scalability, security, and user engagement.
