from django import template

register = template.Library()


# Credit: https://www.caktusgroup.com/blog/2018/10/18/filtering-and-pagination-django/
@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or 
    changed.

    Also removes any empty parameters to keep things neat, so can remove 
    a parameter by setting it to ``""``.

    For example, if on page ``products/?sort=price&direction=asc&page=2``,
    then
    <a href="/things/?{% param_replace page=3 %}">Page 3</a>
    expands to
    <a href="products/?sort=price&direction=asc&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()