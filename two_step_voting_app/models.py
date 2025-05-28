from typing import Any

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

# 1️⃣ নির্বাচন বা সেশন
class VotingSession(models.Model):
    title = models.CharField(max_length=255,default="title")
    description = models.TextField(blank=True,default="description")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    session_Image = models.ImageField(upload_to="session_Image", default="session_Image")

    def __str__(self):
        return self.title

# 2️⃣ যে বিষয়গুলোতে ভোট হবে
class Topic(models.Model):
    session = models.ForeignKey(VotingSession, on_delete=models.CASCADE, related_name='topics',default=1)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='topics/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


# 3️⃣ প্রথম ধাপ
class FirstStep(models.Model):
    session = models.OneToOneField(VotingSession, on_delete=models.CASCADE, related_name='first_step',default=1)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.session.title

# 4️⃣ দ্বিতীয় ধাপ
class SecondStep(models.Model):
    session = models.OneToOneField(VotingSession, on_delete=models.CASCADE, related_name='second_step',default=1)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.session.title


# 5️⃣ First Step Vote
class FirstStepVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(VotingSession, on_delete=models.CASCADE, related_name='first_step_Vote',default=1)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # একজন ইউজার সর্বোচ্চ ২টি ভোট দিতে পারবে
        user_votes = FirstStepVote.objects.filter(user=self.user, session=self.session)
        if user_votes.count() >= 3:
            raise ValidationError("আপনি সর্বোচ্চ ২টি ভোট দিতে পারবেন।")

        # একই টপিকে একাধিক ভোট যেন না দিতে পারে
        if user_votes.filter(topic=self.topic).exists():
            raise ValidationError("আপনি এই টপিকে ইতোমধ্যে ভোট দিয়েছেন।")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} voted {self.topic.title}"
# 6️⃣ Second Step Vote
class SecondStepVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(VotingSession, on_delete=models.CASCADE, related_name='second_step_Vote',default=1)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # একজন ইউজার শুধুমাত্র ১টি ভোট দিতে পারবে
        if SecondStepVote.objects.filter(user=self.user, session=self.session).exists():
            raise ValidationError("আপনি ইতোমধ্যে একটি ভোট দিয়েছেন।")

        # একই টপিকে আবার যেন না দিতে পারে
        if SecondStepVote.objects.filter(user=self.user, topic=self.topic).exists():
            raise ValidationError("আপনি এই টপিকে ইতোমধ্যে ভোট দিয়েছেন।")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} voted {self.topic.title}"
