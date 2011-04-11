from django.template import Library, Node, TemplateSyntaxError

from ..utils import get_plugin_from_string

register = Library()


class PluginsNode(Node):
    def __init__(self, point_name, var_name):
        self.plugins = get_plugin_from_string(point_name).get_plugins()
        self.var_name = var_name

    def render(self, context):
        context[self.var_name] = self.plugins
        return ''


@register.tag
def get_plugins(parser, token):
    contents = token.split_contents()
    if len(contents) != 4:
        raise TemplateSyntaxError("%r tag requires exactly 3 arguments" %
                                  (contents[0]))
    if 'as' != contents[2]:
        raise TemplateSyntaxError("%r tag 2nd argument must be 'as'" %
                                  (contents[0]))
    return PluginsNode(contents[1], contents[3])
