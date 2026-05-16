from django.contrib import admin
from .models import (
    User, Artist, Album, Track, Playlist, Like, Stream,
    Podcast, PodcastEpisode, AudioBook, AudioBookChapter,
    AudioPlay, AudioPlayAct, Poem
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'status', 'joined_date')
    list_filter = ('role', 'status')
    search_fields = ('username', 'email')

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator_type', 'is_verified', 'created_at')
    list_filter = ('creator_type', 'is_verified')
    search_fields = ('name',)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    search_fields = ('title', 'artist__name')

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist_name', 'category', 'plays', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'artist_name')

@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'host', 'created_at')

@admin.register(PodcastEpisode)
class PodcastEpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'podcast_series', 'episode_number')

@admin.register(AudioBook)
class AudioBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')

@admin.register(AudioBookChapter)
class AudioBookChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'book', 'chapter_number')

@admin.register(AudioPlay)
class AudioPlayAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'created_at')

@admin.register(AudioPlayAct)
class AudioPlayActAdmin(admin.ModelAdmin):
    list_display = ('title', 'play', 'act_number')

@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = ('title', 'poet')

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_public', 'created_at')
    list_filter = ('is_public',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'created_at')

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'played_at')

