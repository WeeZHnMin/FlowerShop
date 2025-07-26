from django.contrib import admin
from .models import Flower

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'usage', 'season', 'price', 'stock')
    search_fields = ('name', 'usage', 'season')
    list_editable = ('price', 'stock')
