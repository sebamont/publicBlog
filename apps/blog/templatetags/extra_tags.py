from django import template
from apps.blog.models import Tag,Type,Category

register = template.Library()

@register.simple_tag
def get_category_list():
    category = Category.objects.all()
    return category

@register.simple_tag
def get_type_list():
    types = Type.objects.all()
    return types

@register.simple_tag
def get_tag_list():
    tags = Tag.objects.all()
    return tags