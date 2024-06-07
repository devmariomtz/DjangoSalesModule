from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_sesion, name='index'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('gestionar_cotizaciones/', views.gestionar_cotizaciones, name='gestionar_cotizaciones'),
    path('eliminar_cotizacion/<str:id>/', views.eliminar_cotizacion, name='eliminar_cotizacion'),
    path('editar_cotizacion/<str:id>/', views.editar_cotizacion, name='editar_cotizacion'),
    path('detalle_cotizacion/<str:id>/', views.detalle_cotizacion, name='detalle_cotizacion'),
    path('gestionar_proveedores/', views.gestionar_proveedores, name='gestionar_proveedores'),
    path('crear_proveedor/', views.crear_proveedor, name='crear_proveedor'),
    path('editar_proveedor/<str:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar_proveedor/<str:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('detalle_proveedor/<str:id>/', views.detalle_proveedor, name='detalle_proveedor'),
    path('gestionar_productos/', views.gestionar_productos, name='gestionar_productos'),
    path('registrar_producto/', views.registrar_producto, name='registrar_producto'),
    path('editar_producto/<str:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<str:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('detalle_producto/<str:id>/', views.detalle_producto, name='detalle_producto'),
    path('crear_orden/', views.crear_orden_view, name='crear_orden'),
    path('obtener_productos/', views.obtener_productos, name='obtener_productos'),
    path('aceptar_cotizacion/<str:id>/', views.aceptar_cotizacion, name='aceptar_cotizacion'),
    path('denegar_cotizacion/<str:id>/', views.denegar_cotizacion, name='denegar_cotizacion'),
]













