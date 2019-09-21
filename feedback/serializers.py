from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=50)
    comment = serializers.CharField(max_length=8000)

    class Meta:
        model = Feedback
        fields = '__all__'

    def create(self, validated_data):
        return Feedback.objects.create(**validated_data)

