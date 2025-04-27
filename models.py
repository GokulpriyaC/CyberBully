from django.db import models
from django.contrib.auth.models import User

# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instaid = models.CharField(max_length=100)
    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reported_profile = models.CharField(max_length=255)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    blockchain_tx_hash = models.CharField(max_length=255, blank=True, null=True)  # Store Ethereum TX hash

    def __str__(self):
        return f"Report on {self.reported_profile} by {self.user.username}"