from django import template

from posts.models import Post

register = template.Library()


class RecentPostsNode(template.Node):
    def __init__(self, count: str, varname: str = 'recent_posts'):
        self.count = int(count)
        self.varname = varname
    def render(self, context):
        recent_posts = Post.objects.order_by('-date_created')[:self.count]
        context[self.varname] = recent_posts
        return ''


@register.tag
def get_recent_posts(parser, token):
    try:
        tag_name, count, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('Invalid arguments for recent_posts tag')
    return RecentPostsNode(count, varname)
