from django.contrib import admin
from .models import Category, Tag, Quiz, QuizTag

class QuizTagInline(admin.TabularInline):
    model = QuizTag
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'status', 'is_public', 'created_by', 'created_at')
    list_filter = ('difficulty', 'status', 'is_public', 'category')
    search_fields = ('title', 'topic', 'description')
    inlines = [QuizTagInline]
    readonly_fields = ('created_at', 'updated_at')
