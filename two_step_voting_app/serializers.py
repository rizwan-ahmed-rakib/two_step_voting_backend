from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Topic, FirstStepVote, SecondStepVote

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class FirstStepVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstStepVote
        fields = '__all__'

class SecondStepVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondStepVote
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user