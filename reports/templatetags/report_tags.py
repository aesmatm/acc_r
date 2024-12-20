from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the arg and value"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def currency(value):
    """Format value as currency"""
    try:
        return "{:,.2f} ج.م".format(float(value))
    except (ValueError, TypeError):
        return "0.00 ج.م"
