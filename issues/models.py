from collections import defaultdict
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.html import escape, format_html
from django.urls import reverse
from core.models import TimeStampedModel
from core.utils import unique_slugify


class Issue(models.Model):
    text = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        )
    slug = models.SlugField(max_length=255, null=False, blank=True, unique=True)
    active = models.BooleanField(default=True)
    comments = models.ManyToManyField('Comment', through='Tag', related_name='issues')

    def issue_count(self):
        return self.comments.all().count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.text))
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('issue-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.text


class Tag(TimeStampedModel):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

    def __str__(self):
        return '#' + str(self.issue) + ': ' + str(self.comment)


class Comment(TimeStampedModel):
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    slug = models.SlugField(max_length=255, null=False, blank=True, unique=True)

    def hashtag_list(self):
        '''
        Returns a list of unique 'hashtag' strings
        '''
        hashtag_list = []
        for word in self.text.split():
            if word[0] == '#' and len(word) > 1:
                # Remove the hash character and limit length to 255
                hashtag_list.append(word[1:255])
        return list(set(hashtag_list))
 
    def create_issue_dict(self, hashtag_list, hash_char=False):
        '''
        Creates an Issue for each unique hashtag if not present
        Returns a dict {'hashtag': Issue}
        '''
        issue_dict = Issue.objects.in_bulk(hashtag_list, field_name='text')
        for hashtag in hashtag_list:
            if hashtag not in issue_dict:
                issue = Issue(text=hashtag)
                issue.save()
                issue_dict[hashtag] = issue
        return {'#'+key: value for key, value in issue_dict.items()} if hash_char else issue_dict
    
    def get_self_tag_dict(self):
        '''
        Returns {'hashtag': [Tags]}
        '''
        dict = defaultdict(list)
        for tag in self.tag_set.all():
            dict[tag.issue.text].append(tag)
        return dict

    def create_tags(self):
        '''
        Creates Issues where necessary
        Deletes and Creates Tags according to the current state of self.hashtag_list()
        Returns a list of the new tags created
        '''
        hashtag_list = self.hashtag_list()
        tag_dict = self.get_self_tag_dict()
        issue_dict = self.create_issue_dict(hashtag_list)
        new_tags = []
        
        # Remove redundant tags
        for key, values in tag_dict.items():
            if key not in hashtag_list:
                for tag in values:
                    tag.delete()
        
        # Create missing tags
        for hashtag in hashtag_list:
            if hashtag not in tag_dict:
                issue = issue_dict[hashtag]
                tag = Tag(comment=self, issue=issue)
                tag.save()
                new_tags.append(tag)
        
        return new_tags
    
    def get_text_links(self):
        '''
        Adds links to issues for each #word in self.text
        '''
        text = escape(self.text)
        hashtag_dict = self.create_issue_dict(self.hashtag_list(), hash_char=True)
        link = '<a href="{}" class="text-decoration-none">{}</a>'
        output = []
        for word in text.split():
            issue = hashtag_dict.get(word)
            if issue:
                word = format_html(link, issue.get_absolute_url(), word)
            output.append(word)
        return ' '.join(output)

    def short_comment_ellipsis(self, length=20):
        return self.text[:(length-3)] + '...' if len(self.text) > length else self.text
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.text[:20]))
        super().save(*args, **kwargs)
        self.create_tags()

    def get_absolute_url(self):
        return reverse("comment-detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.short_comment_ellipsis(20)
