from django.db import models
from django.conf import settings
from core import TimeStampedModel


class Comment(TimeStampedModel):
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def short_comment(self, length=10):
        return self.text[:(length-3)] + '...' if len(self.text) > length else self.text

    def __str__(self):
        return self.short_comment(10)


class Issue(models.Model):
    text = models.CharField(max_length=255)


class Tag(TimeStampedModel):
    comment = models.ForeignKey(Comment)
    issue = models.ForeignKey(Issue)

    def __str__(self):
        return self.issue + ': ' + self.comment
