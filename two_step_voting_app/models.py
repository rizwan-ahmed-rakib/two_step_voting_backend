from django.db import models
from django.contrib.auth.models import User

# Voting Topic
class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='topics/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# প্রথম ধাপ (First Step) ভোটিং
class FirstStep(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

# প্রথম ধাপে কে কাকে ভোট দিয়েছে
class FirstStepVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

# দ্বিতীয় ধাপ (Second Step) ভোটিং
class SecondStep(models.Model):
    first_step = models.OneToOneField(FirstStep, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)

# দ্বিতীয় ধাপে কে কাকে ভোট দিয়েছে
class SecondStepVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)
