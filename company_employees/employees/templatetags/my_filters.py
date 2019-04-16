from django import template

register = template.Library()


@register.filter(name='query_update')
def query_update(page, query):
    query = query.copy()
    query['page'] = page
    return query.urlencode()
