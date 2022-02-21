from rest_framework import serializers

from app.models import Assignment

class AssignmentSeializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"