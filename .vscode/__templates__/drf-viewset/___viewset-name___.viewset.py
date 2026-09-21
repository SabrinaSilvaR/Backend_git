from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class ___ViewsetName___ViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing ___ViewsetName___ resources.
    """
    permission_classes = [IsAuthenticated]
