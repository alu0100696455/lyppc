from django.contrib import admin

from .models import Alimento
from .models import Cantidad
from .models import Comida

admin.site.register(Alimento)
admin.site.register(Cantidad)
admin.site.register(Comida)
