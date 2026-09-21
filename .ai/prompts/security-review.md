# Prompt: Security Review

Audit Django and DRF configuration and code for security vulnerabilities.

## Checkpoints

1. **Secrets:** Verify `SECRET_KEY` and credentials are not hardcoded or leaked into version control.
2. **Permissions:** Ensure sensitive views have `permission_classes = [IsAuthenticated]`.
3. **ORM Injections:** Verify raw SQL queries (`.raw()` or `cursor.execute()`) are not used with untrusted string formatting.
4. **Input Sanitization:** Verify DRF serializers validate and constrain all incoming request parameters.
5. **Debug Mode:** Verify `DEBUG = False` and restricted `ALLOWED_HOSTS` for production settings.
