from rest_framework import serializers

from taskboard.models import Board, Column, Label


class BoardListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ('pk', 'name', 'is_archived')


class BoardSerializer(serializers.ModelSerializer):
    columns = serializers.PrimaryKeyRelatedField(many=True, queryset=Column.objects.all())
    labels = serializers.PrimaryKeyRelatedField(many=True, queryset=Label.objects.all())

    class Meta:
        model = Board
        fields = ('pk', 'name', 'is_archived', 'columns', 'labels')
