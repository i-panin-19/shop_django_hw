from django import template


register = template.Library()


@register.filter()
def mymedia(val):
     if val:
         return f'/media/{val}'

     return 'https://td-chismetod.ru/img/no-photo_big.png'
