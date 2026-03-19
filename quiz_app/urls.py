from django.contrib import admin
from django.urls import path, include
from common.views import GlobalSearchView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/users/', include('accounts.urls')),
    path('api/v1/', include('quizzes.urls')),
    path('api/v1/', include('questions.urls')),
    path('api/v1/', include('attempts.urls')),
    path('api/v1/interactions/', include('interactions.urls')),
    path('api/v1/analytics/', include('analytics.urls')),
    path('api/v1/search', include([
        path('', GlobalSearchView.as_view({'get': 'list'}), name='global-search'),
    ])),
]
