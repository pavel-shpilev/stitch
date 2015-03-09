from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('name',)


@receiver(post_save, sender=Board)
def create_labels(sender, instance, created, **kwargs):
    """Create labels whenever a board object is created."""
    if created:
        for n in range(6):
            Label.objects.get_or_create(title='Label %s' % str(n+1), board=instance)


class Column(ArchivableMixin, models.Model):
    """
    Giving the project is in Python, List would've been a confusing name.
    """
    title = models.TextField(max_length=50)
    board = models.ForeignKey('Board', related_name='columns')
    order = models.IntegerField()

    def __str__(self):
        return '%s: %s' % (self.pk, self.title)

    class Meta:
        ordering = ('order',)
        order_with_respect_to = 'board'
        unique_together = ('title', 'board')


class Member(ArchivableMixin, models.Model):
    name = models.TextField(max_length=50, unique=True)

    def delete(self, using=None):
        """
        De-assigning a member from his tasks prior to archiving.
        """
        for card in Card.objects.filter(members_in=[self]):
            card.members.remove(card)
        return super(Member, self).delete(using=using)

    def __str__(self):
        return '%s: %s' % (self.pk, self.name)

    class Meta:
        ordering = ('name',)


class Label(models.Model):
    title = models.TextField(max_length=50)
    board = models.ForeignKey('Board', related_name='labels')

    def __str__(self):
        return '%s: %s' % (self.pk, self.title)

    class Meta:
        unique_together = ('title', 'board')


class Card(ArchivableMixin, models.Model):
    title = models.TextField(max_length=50)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    order = models.IntegerField()
    column = models.ForeignKey('Column', related_name='cards')
    members = models.ManyToManyField('Member', related_name='cards')
    label = models.ForeignKey('Label')

    def __str__(self):
        return '%s: %s / %s / %s' % (
            self.pk, self.column.board.name, self.column.title, self.title
        )

    class Meta:
        ordering = ('order',)
        order_with_respect_to = 'column'
