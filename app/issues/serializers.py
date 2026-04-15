from rest_framework import serializers
from .models import Issue

class IssueSerializer(serializers.ModelSerializer):

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long."
            )
        return value
    
    class Meta:
        model = Issue
        fields = '__all__'