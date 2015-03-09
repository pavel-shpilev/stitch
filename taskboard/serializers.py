from rest_framework import serializers

from taskboard.models import Board, Column, Label, Member, Card


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


class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Label


class MemberListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('pk', 'name')


class MemberSerializer(serializers.ModelSerializer):
    cards = serializers.StringRelatedField(many=True)

    class Meta:
        model = Board
        fields = ('pk', 'name', 'cards')


class ColumnListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Column
        fields = ('pk', 'title', 'board', 'order', 'is_archived')


class ColumnSerializer(serializers.ModelSerializer):
    cards = serializers.StringRelatedField(many=True)

    class Meta:
        model = Column
        fields = ('pk', 'title', 'board', 'order', 'is_archived', 'cards')


class CardListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('pk', 'title', 'column', 'order', 'label', 'members')


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Column
        fields = ('pk', 'title', 'description', 'due_date', 'column', 'order', 'label', 'members', 'is_archived')
