from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class GameManager(models.Manager):
    def get_latest(self):
        return self.get_query_set().order_by('-date')[:20]


class Game(models.Model):
    winner = models.ForeignKey(User, related_name='games_won')
    loser = models.ForeignKey(User, related_name='games_lost')
    date = models.DateTimeField(default=datetime.now)

    objects = GameManager()

    def clean(self):
        if (self.winner_id is not None and self.loser_id is not None and
                self.winner_id == self.loser_id):
            raise ValidationError(
                'Winner and loser can\'t be the same person!'
            )

    def __str__(self):
        return '%s beats %s' % (
            self.winner,
            self.loser
        )


class RankManager(models.Manager):
    def get_score_board(self):
        return self.get_query_set().order_by('-rank')


class Rank(models.Model):
    user = models.ForeignKey(User, related_name='rank', unique=True)
    rank = models.IntegerField(default=1000)
    stdev = models.FloatField('standard deviation', default=50)

    objects = RankManager()

    def __str__(self):
        return '%s (%d/%d)' % (
            self.user.username,
            self.rank,
            self.stdev
        )
