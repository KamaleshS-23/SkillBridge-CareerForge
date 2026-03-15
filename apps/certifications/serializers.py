from rest_framework import serializers
from .models import Certification

class CertificationSerializer(serializers.ModelSerializer):
    provider_display = serializers.CharField(source='get_provider_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_level_display', read_only=True)
    
    class Meta:
        model = Certification
        fields = [
            'id', 'name', 'provider', 'provider_display', 'domain', 
            'description', 'registration_url', 'rating', 'duration', 
            'difficulty_level', 'difficulty_display', 'is_active', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class CertificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = [
            'name', 'provider', 'domain', 'description', 
            'registration_url', 'rating', 'duration', 'difficulty_level'
        ]
    
    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 0 and 5.")
        return value
    
    def validate_registration_url(self, value):
        if value and not (value.startswith('http://') or value.startswith('https://')):
            value = 'https://' + value
        return value
