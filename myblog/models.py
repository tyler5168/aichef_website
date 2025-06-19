from django.db import models
from django.contrib.sessions.models import Session

# Create your models here.

class UserBookmark(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    html_table = models.TextField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    # session = models.OneToOneField(Session, on_delete=models.CASCADE)

