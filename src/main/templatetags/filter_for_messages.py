from django import template

register = template.Library()


@register.filter(name="replace_html")
def replace_html(value, arg):
    """Replacing <br> html with space"""
    return value.replace(arg, " ")
