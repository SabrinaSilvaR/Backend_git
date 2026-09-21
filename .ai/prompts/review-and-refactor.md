# Prompt: Review and Refactor

Refactor legacy or monolithic Django views into clean architecture.

## Instructions

1. Identify bloated views containing direct business logic or SQL queries.
2. Extract read queries into functions in `apiGit/selectors.py`.
3. Extract write mutations and business rules into functions in `apiGit/services.py`.
4. Keep the view responsible only for authentication, serializer invocation, and HTTP response.
5. Run existing tests to ensure zero regressions: `.\vgit\Scripts\python.exe manage.py test apiGit`.
