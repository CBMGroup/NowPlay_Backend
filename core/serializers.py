from rest_framework import serializers
from .models import (
    User, Artist, Album, Track, Playlist, Like, Stream,
    Podcast, PodcastEpisode, AudioBook, AudioBookChapter,
    AudioPlay, AudioPlayAct, Poem
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'role', 'avatar_url', 'status', 
            'preferences', 'joined_date', 'is_staff', 'is_active', 'date_joined'
        )
        read_only_fields = ('joined_date', 'date_joined')

class ArtistSerializer(serializers.ModelSerializer):
    tracks_count = serializers.SerializerMethodField()
    albums_count = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = '__all__'

    def get_tracks_count(self, obj):
        return obj.tracks.count()

    def get_albums_count(self, obj):
        return obj.albums.count()

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
    
    # Specialized fields for the user app
    specialized_details = serializers.SerializerMethodField()

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

    def get_specialized_details(self, obj):
        # Check if the track is a specialized type
        if hasattr(obj, 'podcastepisode'):
            episode = obj.podcastepisode
            return {
                'type': 'podcast',
                'series': PodcastSerializer(episode.podcast_series).data if episode.podcast_series else None,
                'episode_number': episode.episode_number,
                'host_name': obj.artist.name if obj.artist else obj.artist_name
            }
        elif hasattr(obj, 'audiobookchapter'):
            chapter = obj.audiobookchapter
            return {
                'type': 'audiobook',
                'book': AudioBookSerializer(chapter.book).data if chapter.book else None,
                'chapter_number': chapter.chapter_number,
                'author_name': obj.artist.name if obj.artist else obj.artist_name
            }
        elif hasattr(obj, 'audioplayact'):
            act = obj.audioplayact
            return {
                'type': 'audioplay',
                'play': AudioPlaySerializer(act.play).data if act.play else None,
                'act_number': act.act_number,
                'director_name': obj.artist.name if obj.artist else obj.artist_name
            }
        elif hasattr(obj, 'poem'):
            poem = obj.poem
            return {
                'type': 'poem',
                'poet_name': poem.poet.name if poem.poet else (obj.artist.name if obj.artist else obj.artist_name)
            }
        return None

# Specialized Serializers

class PodcastSerializer(serializers.ModelSerializer):
    host_name = serializers.ReadOnlyField(source='host.name')
    class Meta:
        model = Podcast
        fields = '__all__'

class PodcastEpisodeSerializer(TrackSerializer):
    podcast_series_details = PodcastSerializer(source='podcast_series', read_only=True)
    class Meta(TrackSerializer.Meta):
        model = PodcastEpisode
        fields = TrackSerializer.Meta.fields + ('podcast_series', 'podcast_series_details', 'episode_number')

class AudioBookSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.name')
    class Meta:
        model = AudioBook
        fields = '__all__'

class AudioBookChapterSerializer(TrackSerializer):
    book_details = AudioBookSerializer(source='book', read_only=True)
    class Meta(TrackSerializer.Meta):
        model = AudioBookChapter
        fields = TrackSerializer.Meta.fields + ('book', 'book_details', 'chapter_number')

class AudioPlaySerializer(serializers.ModelSerializer):
    director_name = serializers.ReadOnlyField(source='director.name')
    class Meta:
        model = AudioPlay
        fields = '__all__'

class AudioPlayActSerializer(TrackSerializer):
    play_details = AudioPlaySerializer(source='play', read_only=True)
    class Meta(TrackSerializer.Meta):
        model = AudioPlayAct
        fields = TrackSerializer.Meta.fields + ('play', 'play_details', 'act_number')

class PoemSerializer(TrackSerializer):
    poet_name = serializers.ReadOnlyField(source='poet.name')
    class Meta(TrackSerializer.Meta):
        model = Poem
        fields = TrackSerializer.Meta.fields + ('poet', 'poet_name')

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
