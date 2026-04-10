from rest_framework import serializers
from .models import User, Artist, Album, Track, Playlist, Like, Stream

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'avatar_url', 'status', 'preferences', 'joined_date')
        read_only_fields = ('joined_date',)

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    artist_name = serializers.ReadOnlyField(source='artist.name')

    class Meta:
        model = Album
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    artist_details = ArtistSerializer(source='artist', read_only=True)
    album_details = AlbumSerializer(source='album', read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = '__all__'

    def get_likes_count(self, obj):
        return obj.likes_received.count()

    def get_is_liked(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            return Like.objects.filter(user=user, track=obj).exists()
        return False

class PlaylistSerializer(serializers.ModelSerializer):
    tracks_details = TrackSerializer(source='tracks', many=True, read_only=True)
    user_name = serializers.ReadOnlyField(source='user.username')
    track_count = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = '__all__'
        read_only_fields = ('user',)

    def get_track_count(self, obj):
        return obj.tracks.count()

    def get_cover_url(self, obj):
        first_track = obj.tracks.first()
        if first_track:
            return first_track.cover_url
        return None

class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = '__all__'
        read_only_fields = ('user',)
