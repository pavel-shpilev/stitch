from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


LABELS_PER_BOARD = 6


class ArchivableMixin(models.Model):
    """
    Replaces delete operation with archiving.
    """
    is_archived = models.BooleanField(default=False)

    def delete(self, using=None):
        self.is_archived = True
        self.save()

    class Meta:
        abstract = True


class Board(ArchivableMixin, models.Model):
    name = models.TextField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)


@receiver(post_save, sender=Board)
def create_labels(sender, instance, created, **kwargs):
    """Create labels whenever a board object is created."""
    if created:
        for n in range(LABELS_PER_BOARD):
            Label.objects.get_or_create(title='Label {}'.format(n+1), board=instance)


class Column(ArchivableMixin, models.Model):
    """
    Giving the project is in Python, List would've been a confusing name.
    """
    name = models.TextField(max_length=50)
    board = models.ForeignKey('Board')
    order = models.IntegerField()

    class Meta:
        ordering = ('order',)
        order_with_respect_to = 'board'
        unique_together = ('name', 'board')


class Member(ArchivableMixin, models.Model):
    name = models.TextField(max_length=50, unique=True)

    def delete(self, using=None):
        """
        De-assigning a member from his tasks prior to archiving.
        """
        for card in Card.objects.filter(members_in=[object]):
            card.members.remove(card)
        return super(Member, self).delete(using=using)

    class Meta:
        ordering = ('name',)


class Label(models.Model):
    title = models.TextField(max_length=50)
    board = models.ForeignKey('Board')

    class Meta:
        ordering = ('title',)
        order_with_respect_to = 'board'
        unique_together = ('title', 'board')


class Card(ArchivableMixin, models.Model):
    title = models.TextField(max_length=50)
    description = models.TextField()
    due_date = models.DateField()
    order = models.IntegerField()
    column = models.ForeignKey('Column')
    members = models.ManyToManyField('Member')
    label = models.ForeignKey('Label')

    class Meta:
        ordering = ('order',)
        order_with_respect_to = 'column'
