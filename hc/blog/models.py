from django.db import models
from django.utils import timezone
from django.db.models import permalink
from django.contrib.auth.models import User


class Post(models.Model):
    """
    This class represents the Post table in the database.
    """
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=False)
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    category = models.ForeignKey('Category', blank=True)
    publish = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        # print('bug: %s') % self.slug
        return ('view_blog_post', None, {'slug': self.slug})

    class Meta:
        """helper class for ordering the posts"""
        ordering = ('-publish', )

class Category(models.Model):
    """
    This class represents the Category table in the database.
    """
    title = models.CharField(max_length=100, db_index=True, unique=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)

    def __unicode__(self):
        return '%s' % self.title
    
    @permalink
    def get_absolute_url(self):
        return ('view_blog_category', None, {'slug': self.slug})
