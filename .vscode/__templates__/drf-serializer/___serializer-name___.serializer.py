from rest_framework import serializers

class ___SerializerName___Serializer(serializers.Serializer):
    """
    ___SerializerName___ serializer.
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)
    is_active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(read_only=True)

    def validate_name(self, value: str) -> str:
        clean_value = value.strip()
        if not clean_value:
            raise serializers.ValidationError("Name cannot be empty.")
        return clean_value
