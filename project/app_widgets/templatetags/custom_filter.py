from django import template

register = template.Library()


@register.filter
def instance_of(value, arg):
    """Retourne True si l'objet 'value' est une instance de la classe spécifiée dans 'arg'."""
    try:
        # Récupérer la classe dynamique à partir du nom de la chaîne
        clazz = getattr(__import__(arg.split(".")[0]), arg.split(".")[1])
        return isinstance(value, clazz)
    except (AttributeError, TypeError):
        return False
