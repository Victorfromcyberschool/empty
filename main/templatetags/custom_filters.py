from django import template

register  = template.Library()

@register.filter(name='price')
def price(value):
    """
    цена со знаком рубля
    """
    if value is None:
        return 'ноль деняк'
    return f'{value:,} Р'.replace(',', ' ')
