from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    UserRegisterView, ArtistList, ArtistDetail, 
    AlbumList, AlbumDetail, TrackList, TrackDetail, 
    PlaylistViewSet, LikeToggle, StreamCreate, 
    RecommendationView, DashboardStatsView, AnalyticsView, UserViewSet
)

router = DefaultRouter()
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('artists/', ArtistList.as_view(), name='artist-list'),
    path('artists/<int:pk>/', ArtistDetail.as_view(), name='artist-detail'),
    path('albums/', AlbumList.as_view(), name='album-list'),
    path('albums/<int:pk>/', AlbumDetail.as_view(), name='album-detail'),
    path('tracks/', TrackList.as_view(), name='track-list'),
    path('tracks/<int:pk>/', TrackDetail.as_view(), name='track-detail'),
    path('tracks/<int:track_id>/like/', LikeToggle.as_view(), name='like-toggle'),
    path('streams/', StreamCreate.as_view(), name='stream-create'),
    path('recommendations/', RecommendationView.as_view(), name='recommendation-list'),
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('analytics/', AnalyticsView.as_view(), name='analytics-data'),
]
