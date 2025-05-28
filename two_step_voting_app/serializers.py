from rest_framework import serializers
from .models import (
    VotingSession, Topic, FirstStep, SecondStep,
    FirstStepVote, SecondStepVote
)
from django.contrib.auth.models import User

# ইউজার সিরিয়ালাইজার (শুধু নাম দেখানোর জন্য)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# Topic Serializer
class TopicSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Topic
        fields = ['id','session', 'title', 'description', 'image', 'created_by', 'created_at']

# First Step Serializer
class FirstStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstStep
        fields = ['start_time','session', 'end_time', 'is_active']

# Second Step Serializer
class SecondStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondStep
        fields = ['start_time','session', 'end_time', 'is_active']

# Voting Session Serializer (main session info)
class VotingSessionSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    topics = TopicSerializer(many=True, read_only=True)
    first_step = FirstStepSerializer(read_only=True)
    second_step = SecondStepSerializer(read_only=True)

    class Meta:
        model = VotingSession
        fields = [
            'id', 'title','session_Image', 'description', 'created_by', 'created_at',
            'topics', 'first_step', 'second_step'
        ]

# First Step Vote Serializer
# class FirstStepVoteSerializer(serializers.ModelSerializer):
#     # user = UserSerializer(read_only=True)
#     # topic = TopicSerializer(read_only=True)
#
#     class Meta:
#         model = FirstStepVote
#         fields = ['id', 'user', 'topic','session', 'voted_at']



class FirstStepVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstStepVote
        fields = '__all__'

    def validate(self, data):
        user = data['user']
        topic = data['topic']
        session = data['session']

        # সর্বোচ্চ ২টি ভোট চেক
        existing_votes = FirstStepVote.objects.filter(user=user, session=session)
        if existing_votes.count() >= 2:
            raise serializers.ValidationError("you have completed your vote! আপনি সর্বোচ্চ ২টি ভোট দিতে পারবেন।")

        # একই টপিকে ভোট দেওয়া হয়েছে কিনা
        if existing_votes.filter(topic=topic).exists():
            raise serializers.ValidationError("আপনি এই টপিকে ইতোমধ্যে ভোট দিয়েছেন।")

        return data

# Second Step Vote Serializer


class SecondStepVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondStepVote
        fields = ['id', 'user', 'topic', 'session', 'voted_at']
        read_only_fields = ['voted_at']  # ভোট দেয়ার সময় অটো যুক্ত হবে

    def validate(self, data):
        user = data['user']
        topic = data['topic']
        session = data['session']

        # একই session-এ user আগেই ভোট দিয়েছে কিনা
        if SecondStepVote.objects.filter(user=user, session=session).exists():
            raise serializers.ValidationError("আপনি ইতোমধ্যে একটি ভোট দিয়েছেন।")

        # একই টপিকে ভোট দিয়েছে কিনা (সেফটি হিসেবে)
        if SecondStepVote.objects.filter(user=user, topic=topic, session=session).exists():
            raise serializers.ValidationError("আপনি এই টপিকে ইতোমধ্যে ভোট দিয়েছেন।")

        return data


# class SecondStepVoteSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     topic = TopicSerializer(read_only=True)
#
#     class Meta:
#         model = SecondStepVote
#         fields = ['id', 'user', 'topic', 'voted_at']
