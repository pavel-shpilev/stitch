from rest_framework import generics

from taskboard.models import Board
from taskboard.serializers import BoardListSerializer, BoardSerializer


class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
