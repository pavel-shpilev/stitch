from rest_framework import serializers

from taskboard.models import Board, Column, Label


class BoardListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ('pk', 'name', 'is_archived')


class BoardSerializer(serializers.ModelSerializer):
    columns = serializers.StringRelatedField(many=True)
    labels = serializers.StringRelatedField(many=True)

    class Meta:
        model = Board
        fields = ('pk', 'name', 'is_archived', 'columns', 'labels')
