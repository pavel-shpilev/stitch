from rest_framework import generics
from rest_framework.response import Response

from taskboard.models import Board, Label
from taskboard.serializers import BoardListSerializer, BoardSerializer, LabelSerializer


class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Boards can only be renamed.
        data = {'name': request.data.get('name', instance.name)}
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class LabelView(generics.RetrieveUpdateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Labels can only be renamed.
        data = {'title': request.data.get('title', instance.title)}
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
