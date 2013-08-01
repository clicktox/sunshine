from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from taxonomy.models import *
from django.utils.encoding import smart_text

register = template.Library()
class RenderCategoryBlockNode(template.Node):
    """Render the comment list directly"""
     
    def __init__(self, slug,template,limit):
        self.slug = slug
        self.template=template
        self.limit = limit

    
    def render(self, context):
        try:
            category  = Category.objects.get(slug=self.slug)
            l = ':%s' % self.limit
            content_list = category.contentcategory_set.all()[:int(self.limit)]
            template_search_list = [
                "taxonomy/blocks/category/%s.html" % category.slug ,
                "taxonomy/blocks/category/generic.html",
                "taxonomy/blocks/generic.html"
            ]
            liststr = render_to_string(template_search_list, {
                                                              "category" : category,
                                                              "limit" : self.limit, 
                                                              "contents" : content_list,
            }, context)
            context.pop()
            return liststr
        except Exception as e:
            return e


@register.tag
def render_category_block(parser, token):
    """
    Render the comment list (as returned by ``{% get_comment_list %}``)
    through the ``comments/list.html`` template

    Syntax::

        {% render_category_block for slug %}
   
    Example usage::

        {% render_category_block for parenting with "/article.html" limit 5 %}

    """
    bits = token.contents.split()
    if len(bits) != 7:
        raise template.TemplateSyntaxError, "get_latest_links tag takes exactly three arguments"
    if bits[1] != 'for':
        raise template.TemplateSyntaxError, "second argument to the get_latest_links tag must be 'for'"
    if bits[3] != 'with':
        raise template.TemplateSyntaxError, "fourth argument to the get_latest_links tag must be 'with'"
    if bits[5] != 'limit':
        raise template.TemplateSyntaxError, "sixth argument to the get_latest_links tag must be 'limit'"
    try:
        limit = int(bits[6])
    except:
        raise template.TemplateSyntaxError, "seventh argument to the get_latest_links tag must be an integer"
    return RenderCategoryBlockNode(bits[2],bits[4],bits[6])