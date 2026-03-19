from rest_framework import serializers
from .models import QuizRating, Follow, Notification

class QuizRatingSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = QuizRating
        fields = ('id', 'user', 'username', 'quiz', 'rating', 'review', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'quiz', 'created_at', 'updated_at')

class FollowSerializer(serializers.ModelSerializer):
    follower_username = serializers.ReadOnlyField(source='follower.username')
    following_username = serializers.ReadOnlyField(source='following.username')

    class Meta:
        model = Follow
        fields = ('id', 'follower', 'follower_username', 'following', 'following_username', 'created_at')
        read_only_fields = ('id', 'follower', 'created_at')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'user', 'title', 'message', 'type', 'reference_id', 'reference_type', 'is_read', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
