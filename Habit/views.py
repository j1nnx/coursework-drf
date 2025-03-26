from rest_framework import generics, permissions

from .pagination import CustomHabitPagination
from .serializers import HabitSerializers
from .models import Habit


class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializers
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomHabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = Habit.objects.filter(is_public=True).order_by('-id')



