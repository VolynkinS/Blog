from django import template
from django.core.cache import cache
from django.db.models import Count, F, Q

from portfolio.models import Category

register = template.Library()


@register.simple_tag()
def get_list_categories():
    return Category.objects.annotate(cnt=Count('projects', filter=Q(projects__is_published=True))).filter(cnt__gt=0)


@register.inclusion_tag('portfolio/list_categories.html')
def show_categories():
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return context
