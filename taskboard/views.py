from rest_framework import generics
from rest_framework.response import Response

from taskboard.models import Board, Label, Member
from taskboard.serializers import BoardListSerializer, BoardSerializer, LabelSerializer, \
    MemberListSerializer, MemberSerializer


class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Boards can only be renamed. Ignore any other data (i.e. is_archived)
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
        # Labels can only be renamed. Ignore any other data (i.e. board)
        data = {'title': request.data.get('title', instance.title)}
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class MemberList(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberListSerializer


class MemberView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Members can only be renamed. Ignore any other data (i.e. task list)
        data = {'name': request.data.get('name', instance.name)}
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
