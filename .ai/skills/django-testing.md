# Skill: Django & DRF Testing Best Practices

Guidelines for writing robust, automated tests using `rest_framework.test.APITestCase`.

## Test Organization

Structure test files inside an `apiGit/tests/` module:
- `apiGit/tests/__init__.py`
- `apiGit/tests/test_models.py`: Model creation, string representation, constraints.
- `apiGit/tests/test_serializers.py`: Validation rules, field serialization.
- `apiGit/tests/test_views.py`: API endpoints, response payloads, status codes, authentication.
- `apiGit/tests/test_services.py`: Domain functions and business edge cases.

## Writing Endpoint Tests with APITestCase

1. **Authentication:**
   - Test both authenticated and unauthenticated scenarios.
   - Use `self.client.force_authenticate(user=user)` for authenticated requests.

2. **Assertions:**
   - Assert precise HTTP status codes: `status.HTTP_200_OK`, `status.HTTP_201_CREATED`, `status.HTTP_400_BAD_REQUEST`, `status.HTTP_401_UNAUTHORIZED`, `status.HTTP_403_FORBIDDEN`.
   - Assert response body keys and values.

3. **Example Test Case:**
   ```python
   from django.contrib.auth.models import User
   from django.urls import reverse
   from rest_framework import status
   from rest_framework.test import APITestCase
   from apiGit.models import Student

   class StudentAPITests(APITestCase):
       def setUp(self):
           self.user = User.objects.create_user(username='testuser', password='password123')
           self.student = Student.objects.create(
               first_name='Ana',
               last_name='Perez',
               email='ana.perez@inacap.cl'
           )
           self.list_url = reverse('student-list')
           self.detail_url = reverse('student-detail', kwargs={'pk': self.student.pk})

       def test_unauthenticated_request_is_rejected(self):
           response = self.client.get(self.list_url)
           self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

       def test_authenticated_user_can_list_students(self):
           self.client.force_authenticate(user=self.user)
           response = self.client.get(self.list_url)
           self.assertEqual(response.status_code, status.HTTP_200_OK)
           self.assertEqual(len(response.data), 1)
           self.assertEqual(response.data[0]['email'], 'ana.perez@inacap.cl')

       def test_create_student_with_invalid_data_returns_400(self):
           self.client.force_authenticate(user=self.user)
           payload = {'first_name': '', 'last_name': 'Perez', 'email': 'not-an-email'}
           response = self.client.post(self.list_url, payload, format='json')
           self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
           self.assertIn('email', response.data)
   ```
