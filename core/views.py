from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q
from django.utils.timezone import now, timedelta
from django.db.models.functions import TruncDate
from .models import User, Artist, Album, Track, Playlist, Like, Stream
from .serializers import (
    UserSerializer, ArtistSerializer, AlbumSerializer, 
    TrackSerializer, PlaylistSerializer, StreamSerializer
)

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get('password'))
        user.save()

class ArtistList(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TrackList(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    def get_queryset(self):
        queryset = Track.objects.all()
        search = self.request.query_params.get('search')
        category = self.request.query_params.get('category')
        
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(artist_name__icontains=search) |
                Q(category__icontains=search)
            )
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset

class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

class PlaylistViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeToggle(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, track_id):
        track = generics.get_object_or_404(Track, id=track_id)
        like, created = Like.objects.get_or_create(user=request.user, track=track)
        
        if not created:
            like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        
        return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)

class StreamCreate(generics.CreateAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        track = serializer.validated_data['track']
        track.plays += 1
        track.save()
        serializer.save(user=self.request.user)

from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    permission_classes = [permissions.IsAuthenticated] # Adjust later

class RecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Basic recommendation logic: 
        # 1. Tracks from categories user has listened to
        # 2. Popular tracks
        user_streams = Stream.objects.filter(user=request.user).values_list('track__category', flat=True).distinct()
        
        recommendations = Track.objects.filter(category__in=user_streams).exclude(
            streams_received__user=request.user
        ).order_by('-plays')[:10]

        if not recommendations:
            recommendations = Track.objects.order_by('-plays')[:10]

        serializer = TrackSerializer(recommendations, many=True, context={'request': request})
        return Response(serializer.data)
class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        return Response({
            'total_users': User.objects.count(),
            'total_tracks': Track.objects.count(),
            'active_artists': Artist.objects.count(),
            'total_streams': Stream.objects.count(),
            'recent_activity': self.get_recent_activity(),
            'top_tracks': TrackSerializer(Track.objects.order_by('-plays')[:5], many=True, context={'request': request}).data
        })

    def get_recent_activity(self):
        streams = Stream.objects.select_related('user', 'track').order_by('-played_at')[:5]
        activity = []
        for s in streams:
            activity.append({
                'id': f'stream_{s.id}',
                'user': s.user.username,
                'action': 'played',
                'track': s.track.title,
                'artist': s.track.artist_name,
                'time': s.played_at
            })
        return activity

class AnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        seven_days_ago = now() - timedelta(days=7)
        streams_over_time = Stream.objects.filter(played_at__gte=seven_days_ago) \
            .annotate(date=TruncDate('played_at')) \
            .values('date') \
            .annotate(streams=Count('id')) \
            .order_by('date')
            
        category_distribution = Track.objects.values('category') \
            .annotate(count=Count('id')) \
            .order_by('-count')
            
        return Response({
            'streams_over_time': list(streams_over_time),
            'category_distribution': list(category_distribution)
        })
