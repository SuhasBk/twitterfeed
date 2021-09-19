from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# one user can have many handles, and one handle can belong to many user
class UserHandlesMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    handle = models.CharField(max_length=50, default="")

    class Meta:
        unique_together = (("user", "handle"))