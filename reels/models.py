from django.db import models
from events.models import Artist
from django.utils import timezone

class Reel(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    video = models.FileField(upload_to='reels/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"{self.artist.name} - {self.caption[:20]}"
