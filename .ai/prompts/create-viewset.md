# Prompt: Create DRF ViewSet / API View

Create an API endpoint handler in `apiGit/views.py`.

## Instructions

1. For standard CRUD, use `viewsets.ModelViewSet` (or `ReadOnlyModelViewSet`).
2. Define `serializer_class` and implement `get_queryset(self)` leveraging selectors to prevent N+1 queries.
3. Configure `permission_classes = [IsAuthenticated]` (or appropriate custom permission).
4. Register the ViewSet in `apiGit/urls.py` using `routers.DefaultRouter()`.
5. Keep views thin: delegate business mutations to `services.py`.
