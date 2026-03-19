from rest_framework import generics, permissions, status, decorators, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.GenericViewSet, viewsets.mixins.RetrieveModelMixin, viewsets.mixins.UpdateModelMixin):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    @decorators.action(detail=False, methods=['get'])
    def quizzes(self, request):
        """Returns quizzes created by the current user."""
        from quizzes.models import Quiz
        from quizzes.serializers import QuizSerializer
        quizzes = Quiz.objects.filter(created_by=request.user)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    @decorators.action(detail=False, methods=['get'])
    def attempts(self, request):
        """Returns attempts made by the current user."""
        from attempts.models import Attempt
        from attempts.serializers import AttemptSerializer
        attempts = Attempt.objects.filter(user=request.user)
        serializer = AttemptSerializer(attempts, many=True)
        return Response(serializer.data)
