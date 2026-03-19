from rest_framework import serializers
from .models import Category, Tag, Quiz, QuizTag
from accounts.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id', 'slug', 'created_at')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('id', 'slug', 'created_at')

class QuizSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = (
            'id', 'title', 'topic', 'description', 'category', 'category_name',
            'created_by', 'created_by_username', 'difficulty', 'status', 'is_public',
            'passing_score', 'time_limit', 'shuffle_questions', 'shuffle_options',
            'allow_skip', 'max_attempts', 'published_at', 'is_active', 'created_at',
            'updated_at', 'tags'
        )
        read_only_fields = ('id', 'created_by', 'status', 'published_at', 'created_at', 'updated_at')

class QuizCreateUpdateSerializer(serializers.ModelSerializer):
    tag_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    )
    generate_with_ai = serializers.BooleanField(write_only=True, default=False)
    num_questions = serializers.IntegerField(write_only=True, default=5, min_value=1, max_value=20)

    class Meta:
        model = Quiz
        fields = (
            'id', 'title', 'topic', 'description', 'category', 'difficulty',
            'is_public', 'passing_score', 'time_limit', 'shuffle_questions',
            'shuffle_options', 'allow_skip', 'max_attempts', 'tag_ids',
            'generate_with_ai', 'num_questions'
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids', [])
        quiz = Quiz.objects.create(**validated_data)
        if tag_ids:
            quiz.tags.set(tag_ids)
        return quiz

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tag_ids is not None:
            instance.tags.set(tag_ids)
        return instance
