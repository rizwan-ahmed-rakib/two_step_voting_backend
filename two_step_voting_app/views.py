from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Topic, FirstStepVote, SecondStepVote, FirstStep, SecondStep
from .serializers import TopicSerializer, FirstStepVoteSerializer, SecondStepVoteSerializer, RegisterSerializer
from django.utils import timezone
from django.db.models import Count

# নতুন টপিক যোগ করার API
class CreateTopicView(generics.CreateAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# প্রথম ধাপে ভোট দেয়ার API
class FirstStepVoteView(generics.CreateAPIView):
    serializer_class = FirstStepVoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        topic_id = request.data.get("topic")

        # Check vote time
        topic = Topic.objects.get(id=topic_id)
        step = FirstStep.objects.filter(topic=topic, is_active=True).first()

        if step and step.start_time <= timezone.now() <= step.end_time:
            # User already voted 2 times?
            vote_count = FirstStepVote.objects.filter(user=user).count()
            if vote_count >= 2:
                return Response({"message": "আপনি সর্বোচ্চ ২ বার ভোট দিতে পারবেন।"}, status=400)

            vote = FirstStepVote.objects.create(user=user, topic=topic)
            return Response({"message": "ভোট সফলভাবে গ্রহণ করা হয়েছে!"})
        return Response({"message": "ভোট দেয়ার সময় শেষ হয়েছে!"}, status=400)

# প্রথম ধাপের বিজয়ী (top 3 topic)
class FirstStepWinnersView(generics.ListAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        vote_counts = FirstStepVote.objects.values('topic').annotate(total=Count('id')).order_by('-total')[:3]
        topic_ids = [v['topic'] for v in vote_counts]
        return Topic.objects.filter(id__in=topic_ids)

# দ্বিতীয় ধাপে ভোট দেয়ার API
class SecondStepVoteView(generics.CreateAPIView):
    serializer_class = SecondStepVoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        topic_id = request.data.get("topic")

        # Check vote time
        topic = Topic.objects.get(id=topic_id)
        step = SecondStep.objects.filter(is_active=True).first()

        if step and step.start_time <= timezone.now() <= step.end_time:
            # Already voted?
            if SecondStepVote.objects.filter(user=user).exists():
                return Response({"message": "আপনি ইতোমধ্যে ভোট দিয়েছেন!"}, status=400)

            vote = SecondStepVote.objects.create(user=user, topic=topic)
            return Response({"message": "দ্বিতীয় ধাপে ভোট সফল হয়েছে!"})
        return Response({"message": "ভোট দেয়ার সময় শেষ!"}, status=400)

# দ্বিতীয় ধাপের বিজয়ী দেখানোর API
class SecondStepWinnerView(generics.RetrieveAPIView):
    serializer_class = TopicSerializer

    def get_object(self):
        top = SecondStepVote.objects.values('topic') \
            .annotate(total=Count('id')) \
            .order_by('-total') \
            .first()
        return Topic.objects.get(id=top['topic']) if top else None





# ✅ বিজয়ী ৩ জনকে second step এ set করা
# def select_first_step_winners():
#     # ভোট গণনা
#     results = FirstStepVote.objects.values('topic') \
#         .annotate(total=Count('id')).order_by('-total')[:3]
#
#     # second step এর জন্য নির্বাচিত
#     for r in results:
#         topic = Topic.objects.get(id=r['topic'])
#         topic.is_selected_for_second_step = True
#         topic.save()
@api_view(['POST'])
@permission_classes([IsAdminUser])
def select_first_step_winners(request):
    results = FirstStepVote.objects.values('topic') \
        .annotate(total=Count('id')).order_by('-total')[:3]

    for r in results:
        topic = Topic.objects.get(id=r['topic'])
        topic.is_selected_for_second_step = True
        topic.save()

    return Response({"message": "First step winners selected successfully!"})
# time validation function
def is_vote_time_valid(step):
    now = timezone.now()
    return step.start_time <= now <= step.end_time


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_in_first_step(request):
    user = request.user
    topic_id = request.data.get("topic_id")

    # Time validation
    vote_session = FirstStep.objects.first()  # or specific one
    if not is_vote_time_valid(vote_session):
        return Response({"error": "ভোটের সময় শেষ!"}, status=403)

    # Vote save
    FirstStepVote.objects.create(user=user, topic_id=topic_id)
    return Response({"message": "✅ আপনার ভোট গ্রহণ করা হয়েছে!"})



@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username ও Password দিতে হবে'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'এই Username আগে থেকেই আছে'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': '✅ User সফলভাবে তৈরি হয়েছে'})


# @api_view(['POST'])
# def register_user(request):
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'message': '✅ User সফলভাবে তৈরি হয়েছে'}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)