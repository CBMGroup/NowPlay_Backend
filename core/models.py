from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('free', 'Free'),
        ('premium', 'Premium'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='free')
    avatar_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=10, default='active')
    preferences = models.JSONField(default=dict, blank=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

class Artist(models.Model):
    CREATOR_TYPES = (
        ('artist', 'Musical Artist'),
        ('host', 'Podcast Host'),
        ('author', 'Author'),
        ('poet', 'Poet'),
        ('director', 'Director'),
    )
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='artist_profile')
    name = models.CharField(max_length=255)
    creator_type = models.CharField(max_length=20, choices=CREATOR_TYPES, default='artist')
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_creator_type_display()})"

class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    cover_url = models.URLField(blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.artist.name}"

class Track(models.Model):
    CATEGORY_CHOICES = (
        ('Music', 'Music'),
        ('Podcast', 'Podcast'),
        ('Education', 'Education'),
        ('Radio', 'Radio'),
        ('Ugandan Music', 'Ugandan Music'),
        ('Audiobooks', 'Audiobooks'),
        ('Poems', 'Poems'),
        ('Audio Plays', 'Audio Plays'),
    )
    title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255, blank=True) # For backward compatibility
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='tracks')
    cover_url = models.URLField(blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    audio_file = models.FileField(upload_to='tracks/')
    duration = models.IntegerField()  # in seconds
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    is_explicit = models.BooleanField(default=False)
    plays = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Specialized Models

class Podcast(models.Model):
    title = models.CharField(max_length=255)
    host = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='podcasts', limit_choices_to={'creator_type': 'host'})
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='podcast_covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PodcastEpisode(Track):
    podcast_series = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='episodes', null=True, blank=True)
    episode_number = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Podcast Episode"

class AudioBook(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='audiobooks', limit_choices_to={'creator_type': 'author'})
    narrator = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='audiobook_covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class AudioBookChapter(Track):
    book = models.ForeignKey(AudioBook, on_delete=models.CASCADE, related_name='chapters', null=True, blank=True)
    chapter_number = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Audiobook Chapter"

class AudioPlay(models.Model):
    title = models.CharField(max_length=255)
    director = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='audio_plays', limit_choices_to={'creator_type': 'director'})
    cast = models.TextField(blank=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='audioplay_covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class AudioPlayAct(Track):
    play = models.ForeignKey(AudioPlay, on_delete=models.CASCADE, related_name='acts', null=True, blank=True)
    act_number = models.PositiveIntegerField(null=True, blank=True)

class Poem(Track):
    poet = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='recorded_poems', limit_choices_to={'creator_type': 'poet'}, null=True, blank=True)

class Playlist(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    description = models.TextField(blank=True)
    tracks = models.ManyToManyField(Track, related_name='playlists')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='likes_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')

class Stream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='streams')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='streams_received')
    played_at = models.DateTimeField(auto_now_add=True)

