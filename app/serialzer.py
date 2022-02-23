from rest_framework import serializers

from app.models import Assignment
import random

class AssignmentSeializer(serializers.ModelSerializer):
    days_practiced = serializers.IntegerField(required=False)
    class Meta:
        model = Assignment
        fields = "__all__"
        
    def create(self, validated_data):
        validated_data['days_practiced'] = random.randint(1,validated_data['days'])
        return super().create(validated_data)