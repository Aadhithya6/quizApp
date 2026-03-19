from rest_framework import serializers
from .models import Question, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'text', 'is_correct', 'order_index', 'image_url')

class OptionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'text', 'order_index', 'image_url')

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'id', 'quiz', 'text', 'explanation', 'difficulty',
            'question_type', 'order_index', 'points', 'image_url',
            'created_at', 'options'
        )

class OptionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'text', 'order_index', 'image_url')

class QuestionPublicSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'id', 'text', 'question_type', 'order_index', 'image_url', 'options'
        )

    def get_options(self, obj):
        # Use shuffled options if provided by the view
        options = getattr(obj, 'shuffled_options', obj.options.all())
        return OptionPublicSerializer(options, many=True).data
