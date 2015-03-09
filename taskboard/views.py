from rest_framework import generics
from rest_framework.response import Response

from taskboard.models import Board, Label, Member, Column, Card
from taskboard.serializers import BoardListSerializer, BoardSerializer, LabelSerializer, \
    MemberListSerializer, MemberSerializer, ColumnListSerializer, ColumnSerializer, \
    CardListSerializer, CardSerializer


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


class ColumnList(generics.ListCreateAPIView):
    serializer_class = ColumnListSerializer

    def get_queryset(self):
        board_id = self.kwargs['board_id']
        return Column.objects.filter(board=board_id)


class ColumnView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Columns can be renamed and reordered. Ignore any other data
        # (i.e. assigning to different board)
        data = {'title': request.data.get('title', instance.title),
                'order': request.data.get('order', instance.order)}
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CardList(generics.ListCreateAPIView):
    serializer_class = CardListSerializer

    def get_queryset(self):
        column_id = self.kwargs['column_id']
        return Card.objects.filter(column=column_id)


class CardView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        # Restrict cards form moving across the boards and assigning another boards' labels.
        column = Column.objects.get(data.get('column'))
        if not column or column.board != instance.column.board:
            del data['column']
        label = Label.objects.get(data.get('label'))
        if not label or label.board != instance.label.board:
            del data['label']
        # Archiving is done via deleting.
        if 'is_archived' in data:
            del data['is_archived']

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
