from django.urls import path
from .views import CreateTopicView, FirstStepVoteView, FirstStepWinnersView, SecondStepVoteView, SecondStepWinnerView, \
    select_first_step_winners, register_user

urlpatterns = [

    path('register/', register_user, name='register_user'),
    path('create-topic/', CreateTopicView.as_view(), name='create-topic'),
    path('first-vote/', FirstStepVoteView.as_view(), name='first-step-vote'),
    path('first-winners/', FirstStepWinnersView.as_view(), name='first-step-winners'),
    path('second-vote/', SecondStepVoteView.as_view(), name='second-step-vote'),
    path('second-winner/', SecondStepWinnerView.as_view(), name='second-step-winner'),
    path('first-step-winners/', select_first_step_winners),

]
