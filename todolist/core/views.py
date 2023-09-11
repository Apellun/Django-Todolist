from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from core.models import User
from core.serializers import UserSerializer, UserAuthSerializer


@method_decorator(csrf_exempt, name="dispatch")
class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserCreateView(CreateAPIView):
    serializer_class = UserAuthSerializer   


class UserUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAuthSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.filter(user=self.request.user, is_deleted=False)