from __future__ import absolute_import

from mycmsproject.plugins import ContentType


class BlogPost(ContentType):
    title = 'Blog post'
    name = 'blog-post'
