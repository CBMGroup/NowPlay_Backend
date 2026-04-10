from django.contrib import admin
from .models import User, Artist, Album, Track, Playlist, Like, Stream

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'status', 'joined_date')
    list_filter = ('role', 'status')
    search_fields = ('username', 'email')

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_verified', 'created_at')
    list_filter = ('is_verified',)
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

