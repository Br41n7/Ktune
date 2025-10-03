from django.db import models
from events.models import Artist
from django.utils import timezone
from accounts.models import User

class Reel(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    video = models.FileField(upload_to='reels/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"{self.artist.name} - {self.caption[:20]}"

class ReelLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reel = models.ForeignKey('Reel', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'reel')

class ReelComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reel = models.ForeignKey('Reel', on_delete=models.CASCADE)
    comment = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
