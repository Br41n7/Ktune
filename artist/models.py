from django.db import models
from django.utils.translation.trans_real import re
from accounts.models import User


class ArtistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stage_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    genre = models.CharField(max_length=100, blank=True)  # e.g. Comedy, Music, Dance
    profile_picture = models.ImageField(upload_to='artist_profiles/', blank=True, null=True)
    followers=models.ManyToManyField(User,
                                     related_name='following_artists',
                                     blank=True
    )
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    def _str_(self):
        return self.stage_name or self.user.username


# class Follow(models.Model):
#     follower=models.ForeignKey(User,related_name='following',on_delete=models.CASCADE)
#     artist=models.ManyToManyField(User,related_name='follower')#related_name='followers',on_delete=models.CASCADE)
#     followed_at=models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together=('follower','artist')

    def _str_(self):
        return f"{self.follower} follows {self.artist}"
