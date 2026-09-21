# Prompt: Create Django / DRF Test

Create automated test cases using `rest_framework.test.APITestCase`.

## Instructions

1. Place tests in `apiGit/tests/` (e.g. `test_views.py`, `test_serializers.py`, `test_services.py`).
2. Set up reusable test fixtures in `setUp(self)`.
3. Test authentication boundaries: verify unauthorized calls receive `401 Unauthorized`.
4. Test validation errors: assert `400 Bad Request` and check that error keys match expected invalid fields.
5. Test happy path: assert `200 OK` or `201 Created` and verify database records exist.
6. Execute tests: `.\vgit\Scripts\python.exe manage.py test apiGit`.
