from django.contrib import admin
from .models import Proveedor, Producto, Usuario, OrdenCompra, DetalleOrden

# Register your models here.
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Usuario)
admin.site.register(OrdenCompra)
admin.site.register(DetalleOrden)
