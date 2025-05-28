from django.contrib.auth.models import User
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from .models import (
    VotingSession, Topic, FirstStep, SecondStep,
    FirstStepVote, SecondStepVote
)
from .serializers import (
    VotingSessionSerializer, TopicSerializer,
    FirstStepSerializer, SecondStepSerializer,
    FirstStepVoteSerializer, SecondStepVoteSerializer, UserSerializer
)

# Voting Session ViewSet
class VotingSessionViewSet(viewsets.ModelViewSet):
    queryset = VotingSession.objects.all().order_by('-created_at')
    serializer_class = VotingSessionSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Topic ViewSet
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all().order_by('-created_at')
    serializer_class = TopicSerializer
    # search_fields = ['session']
    filterset_fields = ['session',]  # ✅ এই ফিল্ড অনুযায়ী ফিল্টার করা যাবে
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]


    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# First Step ViewSet
class FirstStepViewSet(viewsets.ModelViewSet):
    queryset = FirstStep.objects.all()
    serializer_class = FirstStepSerializer
    # permission_classes = [permissions.IsAdminUser]

# Second Step ViewSet
class SecondStepViewSet(viewsets.ModelViewSet):
    queryset = SecondStep.objects.all()
    serializer_class = SecondStepSerializer
    # permission_classes = [permissions.IsAdminUser]

# First Step Vote ViewSet
class FirstStepVoteViewSet(viewsets.ModelViewSet):
    queryset = FirstStepVote.objects.all()
    serializer_class = FirstStepVoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Second Step Vote ViewSet
class SecondStepVoteViewSet(viewsets.ModelViewSet):
    queryset = SecondStepVote.objects.all()
    serializer_class = SecondStepVoteSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]






from rest_framework.views import APIView

class FirstStepWinnersAPIView(APIView):
    def get(self, request):
        session_id = request.query_params.get('session_id')
        session_title = request.query_params.get('session_title')

        # Session অনুসারে টপিক ফিল্টার করুন
        topics = Topic.objects.all()
        if session_id:
            topics = topics.filter(session__id=session_id)
        elif session_title:
            topics = topics.filter(session__title=session_title)

        # ভোট গুনে শীর্ষ ৩টি টপিক নিন
        winners = topics.annotate(vote_count=Count('firststepvote')).order_by('-vote_count')[:3]

        data = [
            {
                'id': topic.id,
                'session_id': topic.session.id,
                'session': topic.session.title,
                'title': topic.title,
                'vote_count': topic.vote_count
            }
            for topic in winners
        ]
        return Response(data)


class FinalWinnerAPIView(APIView):
    def get(self, request):
        session_id = request.query_params.get('session_id')
        session_title = request.query_params.get('session_title')

        # Session অনুযায়ী Topic ফিল্টার করুন
        topics = Topic.objects.all()
        if session_id:
            topics = topics.filter(session__id=session_id)
        elif session_title:
            topics = topics.filter(session__title=session_title)

        # প্রথম ধাপের ভোট অনুযায়ী টপ ৩ নির্বাচন
        top_3 = topics.annotate(
            vote_count=Count('firststepvote')
        ).order_by('-vote_count')[:3]

        # দ্বিতীয় ধাপের ভোট অনুযায়ী চূড়ান্ত বিজয়ী নির্ধারণ
        final_winner = topics.filter(id__in=[t.id for t in top_3]).annotate(
            vote_count=Count('secondstepvote')
        ).order_by('-vote_count').first()

        if final_winner:
            return Response({
                'id': final_winner.id,
                'session_id': final_winner.session.id,
                'session': final_winner.session.title,
                'title': final_winner.title,
                'vote_count': final_winner.vote_count
            })
        else:
            return Response({'message': 'কোনো ভোট পাওয়া যায়নি'}, status=404)

class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username ও Password দিতে হবে'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'এই Username আগে থেকেই আছে'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        return Response({'message': '✅ User সফলভাবে তৈরি হয়েছে'})
