from django.db import models
from django.conf import settings
from core.models import TimeStampedModel


class Issue(models.Model):
    text = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        )
    active = models.BooleanField(default=True)


class Comment(TimeStampedModel):
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def hashtag_list(self):
        hashtag_list = []
        for word in self.text.split():
            if word[0] == '#':
                # Remove the hash character and limit length to 255
                hashtag_list.append(word[1:255])
        return hashtag_list
    
    def create_issues(self):
        '''
        Creates an Issue for each unique hashtag if not present
        Returns a dict {'hashtag': Issue}
        '''
        hashtag_set = set(self.hashtag_list())
        issue_dict = Issue.objects.in_bulk(hashtag_set, field_name='text')
        for hashtag in hashtag_set:
            issue = issue_dict.get(hashtag)
            if not issue:
                issue = Issue(text=hashtag)
                issue.save()
                issue_dict[hashtag] = issue
        return issue_dict
        
    def create_tags(self):
        '''
        One tag will be created for each unique hashtag in self.text
        '''
        issue_dict = self.create_issues() #  {'hashtag': Issue}
        tags_list = []
        for issue in issue_dict.values():
            tag = Tag(comment=self, issue=issue)
            tag.save()
            tags_list.append(tag)
        return tags_list

    def short_comment(self, length=10):
        return self.text[:(length-3)] + '...' if len(self.text) > length else self.text

    def __str__(self):
        return self.short_comment(10)


class Tag(TimeStampedModel):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        )
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE
        )

    def __str__(self):
        return self.issue + ': ' + self.comment
