from django.contrib import admin
from .models import Attempt, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ('question', 'selected_option', 'is_skipped')

@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'attempt_number', 'status', 'score', 'is_passed', 'started_at')
    list_filter = ('status', 'is_passed', 'quiz')
    search_fields = ('user__username', 'quiz__title')
    inlines = [AnswerInline]
    readonly_fields = ('started_at', 'completed_at')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'is_skipped')
    list_filter = ('is_skipped', 'attempt__quiz')
