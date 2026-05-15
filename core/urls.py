from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    UserRegisterView, ArtistList, ArtistDetail, 
    AlbumViewSet, TrackList, TrackDetail, 
    PlaylistViewSet, LikeToggle, StreamCreate, 
    RecommendationView, DashboardStatsView, AnalyticsView, UserViewSet,
    PodcastEpisodeViewSet, AudioBookChapterViewSet, AudioPlayActViewSet, PoemViewSet,
    PodcastViewSet, AudioBookViewSet, AudioPlayViewSet
)

router = DefaultRouter()
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'users', UserViewSet, basename='user')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'podcasts', PodcastEpisodeViewSet, basename='podcastepisode')
router.register(r'podcast-series', PodcastViewSet, basename='podcast')
router.register(r'audiobooks', AudioBookChapterViewSet, basename='audiobookchapter')
router.register(r'audiobook-series', AudioBookViewSet, basename='audiobook')
router.register(r'audioplays', AudioPlayActViewSet, basename='audioplayact')
router.register(r'audioplay-series', AudioPlayViewSet, basename='audioplay')
router.register(r'poems', PoemViewSet, basename='poem')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('artists/', ArtistList.as_view(), name='artist-list'),
    path('artists/<int:pk>/', ArtistDetail.as_view(), name='artist-detail'),
    path('tracks/', TrackList.as_view(), name='track-list'),
    path('tracks/<int:pk>/', TrackDetail.as_view(), name='track-detail'),
    path('tracks/<int:track_id>/like/', LikeToggle.as_view(), name='like-toggle'),
    path('streams/', StreamCreate.as_view(), name='stream-create'),
    path('recommendations/', RecommendationView.as_view(), name='recommendation-list'),
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('analytics/', AnalyticsView.as_view(), name='analytics-data'),
]
