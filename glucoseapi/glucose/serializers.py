from rest_framework import serializers
from glucose.models import GlucoseLevel, GlucoseLevelMetadata

class GlucoseLevelMetadataSerializer(serializers.ModelSerializer):
    """
    Serializer class for the GlucoseLevelMetadata model.
    """
    class Meta:
        model = GlucoseLevelMetadata
        fields = '__all__'

class GlucoseLevelSerializer(serializers.ModelSerializer):
    """
    Serializer class for the GlucoseLevel model.
    """
    class Meta:
        model = GlucoseLevel
        fields = '__all__'
