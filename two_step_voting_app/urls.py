
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VotingSessionViewSet, TopicViewSet,
    FirstStepViewSet, SecondStepViewSet,
    FirstStepVoteViewSet, SecondStepVoteViewSet, RegisterUserView, UsersViewSet, FirstStepWinnersAPIView,
    FinalWinnerAPIView
)

router = DefaultRouter()
router.register('users', UsersViewSet)
router.register('voting-sessions', VotingSessionViewSet)
router.register('topics', TopicViewSet)
router.register('first-step', FirstStepViewSet)
router.register('second-step', SecondStepViewSet)
router.register('first-step-votes', FirstStepVoteViewSet)
router.register('second-step-votes', SecondStepVoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('first-step-winners/', FirstStepWinnersAPIView.as_view()),
    path('final-winner/', FinalWinnerAPIView.as_view()),

]
