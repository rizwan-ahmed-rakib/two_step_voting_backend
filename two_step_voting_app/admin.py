from django.contrib import admin
from .models import Topic, FirstStep, SecondStep, FirstStepVote, SecondStepVote, VotingSession

# Register your models here.
admin.site.register(Topic)
admin.site.register(FirstStep)
admin.site.register(SecondStep)
admin.site.register(FirstStepVote)
admin.site.register(SecondStepVote)
admin.site.register(VotingSession)