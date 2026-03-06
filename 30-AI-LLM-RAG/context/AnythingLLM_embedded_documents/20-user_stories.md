# SQAAILab – User Stories (Flask Blog API + Admin Interface)

## Table of Contents
1. [Product Scope](#product-scope)
2. [Personas](#personas)
3. [Assumptions & Constraints](#assumptions--constraints)
4. [Test Pyramid Mapping (Recommended)](#test-pyramid-mapping-recommended)
5. [Feature: API Health](#feature-api-health)
6. [Feature: Users (CRUD)](#feature-users-crud)
7. [Feature: Posts (CRUD)](#feature-posts-crud)
8. [Feature: Statistics Dashboard (Read)](#feature-statistics-dashboard-read)
9. [Feature: Admin UI (E2E)](#feature-admin-ui-e2e)
10. [Non-Functional / Cross-Cutting Acceptance Criteria](#non-functional--cross-cutting-acceptance-criteria)

---

## Product Scope
The system provides:
- A REST API to manage Users and Posts (blog articles).
- A lightweight Admin UI (single-page HTML + JavaScript) that calls the API.
- A Statistics view summarizing totals.

## Personas
- **Admin**: manages users and posts using the Admin UI.
- **API Consumer (QA/Developer)**: tests the REST API directly (curl/Postman/automation).
- **Stakeholder**: checks global statistics to validate platform activity.

## Assumptions & Constraints
- Backend runs at `http://localhost:5000`.
- API base path: `/api`.
- Database tables are auto-created on backend startup.
- No authentication/authorization is implemented (admin-only prototype).
- Validation implemented:
  - Missing required fields → HTTP 400
  - Duplicate username/email → HTTP 409
  - Resource not found → HTTP 404
  - Server error → HTTP 500
- Data rules:
  - `User.username` is unique.
  - `User.email` is unique.
  - `Post.user_id` must reference an existing user.
  - Deleting a user deletes their posts (cascade).

---

## Test Pyramid Mapping (Recommended)
The **Test Pyramid Principle** suggests: **many unit tests**, **fewer integration tests**, and **very few end-to-end (e2e) tests**.

- **Unit tests**: fast tests for pure validation/serialization/business rules (no HTTP, no real DB).
- **Integration tests**: Flask route + request/response + database behavior (covers most stories here).
- **E2E tests**: browser-based Admin UI flow calling the real API (slowest, keep minimal).

| Story / NFR | Recommended primary test type | Also valuable (keep lean) |
|---|---|---|
| HLTH-01 — Check API availability | Integration (HTTP contract: `/api/health`) | Unit (health handler returns expected JSON shape) |
| USR-01 — Create a user | Integration (POST + DB + uniqueness + password not returned) | Unit (required-field validation; response serialization excludes password/hash) |
| USR-02 — List users | Integration (GET + DB rows → JSON) | Unit (user serialization/ordering if implemented separately) |
| USR-03 — View a user by ID | Integration (GET + 200/404 behavior) | Unit (ID parsing / not-found mapping if implemented as helpers) |
| USR-04 — Delete a user (cascade posts) | Integration (DELETE + DB cascade + 404 behavior) | Unit (none required beyond helper logic; cascade is a DB/integration concern) |
| PST-01 — Create a post | Integration (POST + FK user exists + DB write) | Unit (required-field validation; published default logic; serialization shape) |
| PST-02 — List all posts | Integration (GET + DB ordering) | Unit (ordering function if extracted) |
| PST-03 — List published posts only | Integration (GET with query param + DB filter) | Unit (query-param parsing; filter predicate if extracted) |
| PST-04 — View a post by ID | Integration (GET + 200/404 behavior) | Unit (not-found mapping if extracted) |
| PST-05 — Update a post | Integration (PUT + DB update + `updated_at` refreshed) | Unit (merge/patch logic for allowed fields if implemented separately) |
| PST-06 — Delete a post | Integration (DELETE + DB delete + 404 behavior) | Unit (none required beyond helper logic) |
| STS-01 — View global statistics | Integration (GET + aggregates reflect DB state) | Unit (stat aggregation function if separated from DB layer) |
| NFR-01 — JSON responses and HTTP codes | Integration (smoke contract across endpoints) | Unit (error handler maps exceptions → correct JSON + status) |
| NFR-02 — CORS enabled for Admin UI | Integration (assert CORS headers on API responses) | E2E (single browser test proving UI can call API) |
| NFR-03 — Error handling does not corrupt session | Integration (force error mid-transaction; assert rollback) | Unit (transaction wrapper calls rollback on exception if extracted) |

E2E coverage is intentionally limited to two critical-path stories:
- E2E-01 — Admin UI loads and shows live statistics
- E2E-02 — Admin can create user then create post via UI

---

## Feature: API Health

### Story HLTH-01 — Check API availability
**User Story**
As an API Consumer (QA/Developer), I want to check the health endpoint, so that I can confirm the API is running before executing tests.

**Acceptance Criteria**
Scenario: Health check returns an OK response
- Given the backend server is running
- When I send a GET request to `/api/health`
- Then the response status code is 200
- And the response body contains `status: "ok"` and a non-empty `message`

**Test Cases**
- TC-HLTH-01 (Positive): Start backend; call `GET /api/health`; expect 200 and JSON keys `status`, `message`.
- TC-HLTH-02 (Negative): Stop backend; call `GET /api/health`; expect network/connection failure at client.

---

## Feature: Users (CRUD)

### Story USR-01 — Create a user
**User Story**
As an Admin, I want to create a user with username, email, and password, so that the user can be referenced as an author for posts.

**Acceptance Criteria**
Scenario: Create user with valid input
- Given a username and email that do not already exist
- When I send a POST request to `/api/users` with `username`, `email`, and `password`
- Then the response status code is 201
- And the response contains a `user` object with an `id`, `username`, `email`, and `created_at`
- And the returned user does not expose the password or password hash

Scenario: Reject missing required fields
- Given the request payload is missing `username` or `email` or `password`
- When I send a POST request to `/api/users`
- Then the response status code is 400
- And the response contains `error: "Missing required fields"`

Scenario: Reject duplicate username
- Given a user already exists with the same username
- When I send a POST request to `/api/users` using that username
- Then the response status code is 409
- And the response contains `error: "Username already exists"`

Scenario: Reject duplicate email
- Given a user already exists with the same email
- When I send a POST request to `/api/users` using that email
- Then the response status code is 409
- And the response contains `error: "Email already exists"`

**Test Cases**
- TC-USR-01 (Positive): POST valid user JSON; expect 201 and returned user fields; ensure no password fields present.
- TC-USR-02 (Negative): POST `{username,email}` missing password; expect 400 and correct error.
- TC-USR-03 (Negative): Create user A; POST user B with same username; expect 409.
- TC-USR-04 (Negative): Create user A; POST user B with same email; expect 409.

---

### Story USR-02 — List users
**User Story**
As an Admin, I want to view a list of users, so that I can confirm who exists in the system and use their IDs for posts.

**Acceptance Criteria**
Scenario: Retrieve all users
- Given the backend server is running
- When I send a GET request to `/api/users`
- Then the response status code is 200
- And the response contains a `users` array
- And each user item contains `id`, `username`, `email`, `created_at`

**Test Cases**
- TC-USR-05 (Positive): GET `/api/users`; expect 200 and `users` array.
- TC-USR-06 (Edge): With zero users in DB; GET `/api/users`; expect 200 and `users: []`.

---

### Story USR-03 — View a user by ID
**User Story**
As an Admin, I want to view user details by ID, so that I can verify the correct user exists before managing related posts.

**Acceptance Criteria**
Scenario: Retrieve user details by valid ID
- Given a user exists with ID `X`
- When I send a GET request to `/api/users/X`
- Then the response status code is 200
- And the response contains `user.id = X`

Scenario: User does not exist
- Given no user exists with ID `X`
- When I send a GET request to `/api/users/X`
- Then the response status code is 404
- And the response contains `error: "Not found"`

**Test Cases**
- TC-USR-07 (Positive): Create a user; GET `/api/users/{id}`; expect 200 and matching id.
- TC-USR-08 (Negative): GET `/api/users/999999`; expect 404 and error body.

---

### Story USR-04 — Delete a user
**User Story**
As an Admin, I want to delete a user, so that I can remove obsolete accounts and their related data.

**Acceptance Criteria**
Scenario: Delete a user
- Given a user exists with ID `X`
- When I send a DELETE request to `/api/users/X`
- Then the response status code is 200
- And the response contains `message: "User deleted"`

Scenario: Cascade delete user posts
- Given a user exists with ID `X` and they have posts
- When I delete the user with DELETE `/api/users/X`
- Then the user is removed
- And the user’s posts are removed from the database

Scenario: Delete a non-existent user
- Given no user exists with ID `X`
- When I send a DELETE request to `/api/users/X`
- Then the response status code is 404

**Test Cases**
- TC-USR-09 (Positive): Create user; DELETE `/api/users/{id}`; expect 200; then GET `/api/users/{id}` returns 404.
- TC-USR-10 (Data integrity): Create user; create post for that user; delete user; then GET `/api/posts/{postId}` returns 404.
- TC-USR-11 (Negative): DELETE `/api/users/999999`; expect 404.

---

## Feature: Posts (CRUD)

### Story PST-01 — Create a post
**User Story**
As an Admin, I want to create a post with a title, content, author (user ID), and published flag, so that I can add blog content to the system.

**Acceptance Criteria**
Scenario: Create post with valid input
- Given a user exists with ID `U`
- When I send a POST request to `/api/posts` with `title`, `content`, and `user_id = U`
- Then the response status code is 201
- And the response contains a `post` object with `id`, `title`, `content`, `published`, `author`, `created_at`, `updated_at`

Scenario: Reject missing required fields
- Given the request payload is missing `title` or `content` or `user_id`
- When I send a POST request to `/api/posts`
- Then the response status code is 400
- And the response contains `error: "Missing required fields"`

Scenario: Reject unknown author
- Given no user exists with ID `U`
- When I send a POST request to `/api/posts` with `user_id = U`
- Then the response status code is 404
- And the response contains `error: "User not found"`

**Test Cases**
- TC-PST-01 (Positive): Create user; POST valid post JSON; expect 201 and author username returned.
- TC-PST-02 (Negative): POST missing title; expect 400.
- TC-PST-03 (Negative): POST with user_id not in DB; expect 404 and `User not found`.

---

### Story PST-02 — List all posts
**User Story**
As an Admin, I want to list all posts (draft and published), so that I can review content and manage deletions.

**Acceptance Criteria**
Scenario: Retrieve all posts
- Given the backend server is running
- When I send a GET request to `/api/posts`
- Then the response status code is 200
- And the response contains a `posts` array ordered by `created_at` descending

**Test Cases**
- TC-PST-04 (Positive): Create 2 posts at different times; GET `/api/posts`; expect newest first.
- TC-PST-05 (Edge): With zero posts; GET `/api/posts`; expect 200 and `posts: []`.

---

### Story PST-03 — List published posts only
**User Story**
As a Stakeholder, I want to list only published posts, so that I can review what is considered public content.

**Acceptance Criteria**
Scenario: Filter to published posts
- Given there are both draft and published posts
- When I send a GET request to `/api/posts?published=true`
- Then the response status code is 200
- And every returned post has `published = true`

**Test Cases**
- TC-PST-06 (Positive): Create one draft and one published post; GET `/api/posts?published=true`; expect only published.
- TC-PST-07 (Edge): If no published posts exist; GET `/api/posts?published=true`; expect `posts: []`.

---

### Story PST-04 — View a post by ID
**User Story**
As an Admin, I want to view a post by ID, so that I can verify its content and status.

**Acceptance Criteria**
Scenario: Retrieve post details by valid ID
- Given a post exists with ID `P`
- When I send a GET request to `/api/posts/P`
- Then the response status code is 200
- And the response contains `post.id = P`

Scenario: Post does not exist
- Given no post exists with ID `P`
- When I send a GET request to `/api/posts/P`
- Then the response status code is 404
- And the response contains `error: "Not found"`

**Test Cases**
- TC-PST-08 (Positive): Create post; GET `/api/posts/{id}`; expect 200 and matching id.
- TC-PST-09 (Negative): GET `/api/posts/999999`; expect 404.

---

### Story PST-05 — Update a post
**User Story**
As an Admin, I want to update a post’s title/content/published status, so that I can correct content and manage publication.

**Acceptance Criteria**
Scenario: Update one or more fields
- Given a post exists with ID `P`
- When I send a PUT request to `/api/posts/P` with any of `title`, `content`, `published`
- Then the response status code is 200
- And the returned post reflects the updated fields
- And `updated_at` is refreshed

Scenario: Update non-existent post
- Given no post exists with ID `P`
- When I send a PUT request to `/api/posts/P`
- Then the response status code is 404

**Test Cases**
- TC-PST-10 (Positive): Create post as draft; PUT `/api/posts/{id}` `{published:true}`; expect 200 and published true.
- TC-PST-11 (Positive): PUT update title and content; expect fields changed.
- TC-PST-12 (Negative): PUT `/api/posts/999999`; expect 404.

---

### Story PST-06 — Delete a post
**User Story**
As an Admin, I want to delete a post, so that I can remove outdated or incorrect content.

**Acceptance Criteria**
Scenario: Delete a post
- Given a post exists with ID `P`
- When I send a DELETE request to `/api/posts/P`
- Then the response status code is 200
- And the response contains `message: "Post deleted"`

Scenario: Delete non-existent post
- Given no post exists with ID `P`
- When I send a DELETE request to `/api/posts/P`
- Then the response status code is 404

**Test Cases**
- TC-PST-13 (Positive): Create post; DELETE `/api/posts/{id}`; expect 200; then GET `/api/posts/{id}` returns 404.
- TC-PST-14 (Negative): DELETE `/api/posts/999999`; expect 404.

---

## Feature: Statistics Dashboard (Read)

### Story STS-01 — View global statistics
**User Story**
As a Stakeholder, I want to view global counts of users and posts, so that I can quickly assess platform activity.

**Acceptance Criteria**
Scenario: Retrieve global statistics
- Given the backend server is running
- When I send a GET request to `/api/stats`
- Then the response status code is 200
- And the response contains numeric fields `total_users`, `total_posts`, `published_posts`

Scenario: Stats reflect current data
- Given I create or delete users/posts
- When I request `/api/stats`
- Then the returned totals match the database state

**Test Cases**
- TC-STS-01 (Positive): With empty DB; GET `/api/stats`; expect zeros.
- TC-STS-02 (Data accuracy): Create 2 users, 3 posts (2 published); GET `/api/stats`; expect totals (2, 3, 2).
- TC-STS-03 (Cascade impact): Create user+post; delete user; GET `/api/stats`; expect counts decreased accordingly.

---

## Feature: Admin UI (E2E)

These end-to-end stories intentionally remain **very small in number** (per the Test Pyramid). Most behavior should be validated via **integration tests** against the API; E2E is reserved for proving the Admin UI can drive the critical path in a real browser.

### Story E2E-01 — Admin UI loads and shows live statistics
**User Story**
As an Admin/Stakeholder, I want to open the Admin UI and see live statistics, so that I can quickly confirm the UI-to-API path is working.

**Acceptance Criteria**
Scenario: UI loads and renders stats from the API
- Given the backend server is running at `http://localhost:5000`
- And the Admin UI `index.html` is opened in a browser
- When the Statistics tab is active
- Then the UI requests `GET /api/stats`
- And it renders numeric values for Users, Total Posts, and Published Posts

Scenario: Refresh updates the displayed stats
- Given the Statistics tab is active
- When I click the Refresh button
- Then the UI re-requests `GET /api/stats`
- And the rendered values match the latest API response

**Test Cases (E2E)**
- TC-E2E-01 (Smoke): Start backend; open `index.html`; expect Stats cards to show numbers (not “Loading error”).
- TC-E2E-02 (Refresh): Create or delete data via API (or via UI in another tab); click Refresh; expect stats values to change accordingly.

---

### Story E2E-02 — Admin can create user then create post via UI
**User Story**
As an Admin, I want to create a user and then create a post for that user in the Admin UI, so that I can complete the primary authoring workflow.

**Acceptance Criteria**
Scenario: Create a user via UI and see it listed
- Given the backend server is running
- When I open the Users tab
- And I submit the Create User form with a unique username, email, and password
- Then the UI shows a success message
- And the new user appears in the User List with a visible ID

Scenario: Create a post for the new user via UI and see it listed
- Given the user exists
- When I open the Posts tab
- Then the Author dropdown contains the created user
- When I submit the Create Post form with title/content/author and a selected status
- Then the UI shows a success message
- And the new post appears in the Post List with the correct title and Published/Draft badge

**Test Cases (E2E)**
- TC-E2E-03 (Critical path): Open UI; create a user; navigate to Posts; create a post as Draft; verify it appears with Draft badge.
- TC-E2E-04 (Published variant): Create a post as Published; verify it appears with Published badge.

---

## Non-Functional / Cross-Cutting Acceptance Criteria
These criteria apply across the API stories above.

### NFR-01 — JSON responses and HTTP codes
Scenario: All endpoints return JSON
- Given any API request is processed
- When the API responds
- Then the response content type is JSON
- And the status code matches the documented behavior (200/201/400/404/409/500)

### NFR-02 — CORS enabled for Admin UI
Scenario: Browser-based frontend can call the API
- Given the Admin UI is opened in a browser
- When it calls the API at `http://localhost:5000/api/...`
- Then the browser does not block requests due to CORS

### NFR-03 — Error handling does not corrupt session
Scenario: Internal error triggers rollback
- Given an internal server error occurs during a DB transaction
- When the server returns HTTP 500
- Then the DB session is rolled back
