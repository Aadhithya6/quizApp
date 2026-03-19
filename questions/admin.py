from django.contrib import admin
from .models import Question, Option

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'difficulty', 'question_type', 'order_index', 'points')
    list_filter = ('difficulty', 'question_type', 'quiz')
    search_fields = ('text', 'explanation')
    inlines = [OptionInline]
    ordering = ('quiz', 'order_index')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct', 'order_index')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('text',)
