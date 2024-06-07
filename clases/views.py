import json
from decimal import Decimal
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .forms import (
    DetalleOrdenForm,
    DetalleOrdenFormSet,
    LoginForm,
    OrdenCompraForm,
    ProductoForm,
    ProveedorForm,
)
from .models import DetalleOrden, OrdenCompra, Producto, Proveedor, Usuario,productosDetalleOrden,productosDetalleOrden


# Vista para el inicio de sesión
def inicio_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usuario_id = form.cleaned_data['id'].upper()
            contrasena = form.cleaned_data['contrasena']
            try:
                usuario = Usuario.objects.get(ID=usuario_id, contrasena=contrasena)
                request.session['usuario_id'] = usuario.ID
                request.session['rol'] = usuario.rol
                messages.success(request, f'Bienvenido {usuario.nombre} {usuario.apellido}')
                return redirect('gestionar_cotizaciones')
            except Usuario.DoesNotExist:
                messages.error(request, 'Usuario o contraseña incorrecta')
        else:
            messages.error(request, 'Formato de ID inválido. Por favor, verifica los datos ingresados.')
    else:
        form = LoginForm()

    return render(request, 'inicio_sesion.html', {'form': form})

# Vista para cerrar sesión
def cerrar_sesion(request):
    try:
        del request.session['usuario_id']
        del request.session['rol']
    except KeyError:
        pass
    return redirect('inicio_sesion')

# Vista para gestionar cotizaciones
def gestionar_cotizaciones(request):
    query = request.GET.get('q')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    estado = request.GET.get('estado')
    costo_min = request.GET.get('costo_min')
    costo_max = request.GET.get('costo_max')

    cotizaciones = OrdenCompra.objects.all()

    if query:
        cotizaciones = cotizaciones.filter(
            Q(ID__icontains=query) | Q(proveedor__nombre__icontains=query)
        )

    if fecha_inicio:
        cotizaciones = cotizaciones.filter(fecha_creacion__gte=fecha_inicio)

    if fecha_fin:
        cotizaciones = cotizaciones.filter(fecha_creacion__lte=fecha_fin)

    if estado:
        cotizaciones = cotizaciones.filter(estado=estado)

    if costo_min:
        cotizaciones = cotizaciones.filter(total__gte=costo_min)

    if costo_max:
        cotizaciones = cotizaciones.filter(total__lte=costo_max)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'gestionar_cotizaciones.html', {'cotizaciones': cotizaciones})

    return render(request, 'gestionar_cotizaciones.html', {'cotizaciones': cotizaciones})

# Vista para eliminar una cotización
def eliminar_cotizacion(request, id):
    cotizacion = get_object_or_404(OrdenCompra, ID=id)
    cotizacion.delete()
    return redirect('gestionar_cotizaciones')

# Vista para editar una cotización
def editar_cotizacion(request, id):
    cotizacion = get_object_or_404(OrdenCompra, ID=id)
    if request.method == 'POST':
        form = OrdenCompraForm(request.POST, instance=cotizacion)
        if form.is_valid():
            form.save()
            return redirect('gestionar_cotizaciones')
    else:
        form = OrdenCompraForm(instance=cotizacion)
    return render(request, 'editar_cotizacion.html', {'form': form})

# Vista para ver el detalle de una cotización
def detalle_cotizacion(request, id):
    cotizacion = get_object_or_404(OrdenCompra, ID=id)
    detalle = productosDetalleOrden.objects.filter(orden=cotizacion)  
    # traer todos los productos de la base de datos que estan en el detalle de la orden
    lista = []
    for item in detalle:
        producto = Producto.objects.get(ID=item.producto.ID)
        producto.cantidad = item.cantidad
        producto.subtotal = item.subtotal
        lista.append(producto)
    print('----------------lista----------------')
    print(lista)
    return render(request, 'detalle_cotizacion.html', {'cotizacion': cotizacion, 'productos': lista})

# Vista para gestionar proveedores
def gestionar_proveedores(request):
    query = request.GET.get('q')
    if query:
        proveedores = Proveedor.objects.filter(Q(nombre__icontains=query) | Q.tipo_servicio__icontains(query))
    else:
        proveedores = Proveedor.objects.all()
    return render(request, 'gestionar_proveedores.html', {'proveedores': proveedores})

# Vista para crear un proveedor
def crear_proveedor(request):
    if request.method == 'POST':
        print("request.POST")
        print(request.POST)
        # antes de llamar a ProveedorForm, se deben eliminar la validacion para el campo telefono


        form = ProveedorForm(request.POST)
        print("form")
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor agregado con éxito')
            return redirect('gestionar_proveedores')
        else:
            messages.error(request, 'Por favor, corrija los errores a continuación.')
    else:
        form = ProveedorForm()
    return render(request, 'agregar_proveedor.html', {'form': form})

# Vista para editar proveedor
def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, ID=id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('gestionar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'editar_proveedor.html', {'form': form, 'proveedor': proveedor})

# Vista para ver detalle de proveedor
def detalle_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, ID=id)
    return render(request, 'detalle_proveedor.html', {'proveedor': proveedor})

# Vista para eliminar proveedor
def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, ID=id)
    proveedor.delete()
    return redirect('gestionar_proveedores')

# Vista para gestionar productos
# Vista para gestionar productos
def gestionar_productos(request):
    productos = Producto.objects.all()
    form = ProductoForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['nombre']:
            productos = productos.filter(nombre__icontains=form.cleaned_data['nombre'])
        if form.cleaned_data['categoria']:
            productos = productos.filter(categoria__icontains=form.cleaned_data['categoria'])
        if form.cleaned_data['precio_min']:
            productos = productos.filter(precio__gte=form.cleaned_data['precio_min'])
        if form.cleaned_data['precio_max']:
            productos = productos.filter(precio__lte=form.cleaned_data['precio_max'])
        if form.cleaned_data['proveedor']:
            productos = productos.filter(proveedor=form.cleaned_data['proveedor'])
    return render(request, 'gestionar_productos.html', {'productos': productos, 'form': form})

# Vista para registrar un nuevo producto
def registrar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['message'] = 'Producto registrado con éxito.'
            return redirect('gestionar_productos')
    else:
        form = ProductoForm()

    message = request.session.pop('message', None)
    return render(request, 'registrar_producto.html', {'form': form, 'message': message})

# Vista para editar un producto existente
def editar_producto(request, id):
    producto = get_object_or_404(Producto, ID=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('gestionar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form})

# Vista para eliminar un producto
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, ID=id)
    producto.delete()
    return redirect('gestionar_productos')

# Vista para ver el detalle de un producto
def detalle_producto(request, id):
    producto = get_object_or_404(Producto, ID=id)
    return render(request, 'detalle_producto.html', {'producto': producto})

# Vista para crear una nueva orden
def crear_orden_view(request):
    if (request.method == 'POST'):
        print('-------------request.method-----------------')
        print(request.method)
        print('-------------request.POST-----------------')
        print(request.POST)
        # pintar la lista de los productos
        # hacer una lista con los productos que viene en el request.POST en formato json ['[{"producto":"P123","cantidad":"2"}]']
        productos = json.loads(request.POST.get('productos'))  
        # print('-------------productos-----------------')
        # print(productos)
        
        form = OrdenCompraForm(request.POST)
    
        # Añade los campos ocultos necesarios al request.POST
        # request.POST['productos_detalle_orden-TOTAL_FORMS'] = '1'
        # request.POST['productos_detalle_orden-INITIAL_FORMS'] = '0'
        # request.POST['productos_detalle_orden-MIN_NUM_FORMS'] = '0'
        # request.POST['productos_detalle_orden-MAX_NUM_FORMS'] = '1000'
        # print('----beforeinstanciate----')
        # formset = DetalleOrdenFormSet(request.POST, request.FILES)

        # print('----------------detalleordenformset----------------')
        # print(formset)    

        if form.is_valid():
            try:
                with transaction.atomic():
                    orden = form.save()
                    
                    # formset.instance = orden
                    # formset.save()

                   
        
                    total = request.POST.get('total')  # Obtener el total del formulario
                    orden.total = total
                    orden.save()

                    detalle_orden = DetalleOrden.objects.create(
                        orden=orden,
                        subtotal=total
                    )
                    detalle_orden.save()

                     # guardar el detalle de la orden que tiene estos campos: orden_id, subtotal
                    for producto in productos:
                        # traer el producto de la base de datos con al id del producto que viene en el request.POST
                        productoInstance = Producto.objects.get(ID=producto['producto'])

                        detalle_orden = productosDetalleOrden.objects.create(
                            orden=orden,
                            producto=productoInstance,
                            cantidad=Decimal(str(producto['cantidad'])),
                            subtotal=Decimal(str(producto['subtotal'])),
                            precio_unitario=Decimal(str(producto['precio']))
                        )
                        detalle_orden.save()
                    messages.success(request, 'Orden creada con éxito.')
                    return redirect('gestionar_cotizaciones')
            except Exception as e:
                form = OrdenCompraForm()
                formset = DetalleOrdenForm()
                productos_formset = DetalleOrdenFormSet()
                print("Error al guardar la orden:", e)
                messages.error(request, 'Ocurrió un error al guardar la orden. Intente nuevamente.')
        else:
            # Imprimir errores del formulario y del formset
            print("Form errors:", form.errors)
            # print("Formset errors:", formset.errors)
            # for form in formset:
            #     print("DetalleOrden form errors:", form.errors)
            form = OrdenCompraForm()
            formset = DetalleOrdenForm()
            productos_formset = DetalleOrdenFormSet()
            messages.error(request, 'Por favor, corrija los errores a continuación.')
    else:
        form = OrdenCompraForm()
        formset = DetalleOrdenForm()
        productos_formset = DetalleOrdenFormSet()


    context = {
        'form': form,
        'formset': formset,
        'proveedores': Proveedor.objects.all(),
        'productos_formset': productos_formset,
    }
    return render(request, 'crear_orden.html', context)

def obtener_productos(request):
    proveedor_id = request.GET.get('proveedor_id')
    if proveedor_id:
        productos = Producto.objects.filter(proveedor_id=proveedor_id).values('ID', 'nombre', 'precio')
        return JsonResponse(list(productos), safe=False)
    else:
        return JsonResponse({'error': 'Proveedor no válido'}, status=400)


# def detalle_cotizacion(request, id):
#     cotizacion = get_object_or_404(OrdenCompra, ID=id)
#     return render(request, 'detalle_cotizacion.html', {'cotizacion': cotizacion})

def aceptar_cotizacion(request, id):
    cotizacion = get_object_or_404(OrdenCompra, ID=id)
    cotizacion.estado = 'Aceptado'
    cotizacion.save()
    messages.success(request, 'Cotización aceptada con éxito.')
    return redirect(reverse('gestionar_cotizaciones'))

def denegar_cotizacion(request, id):
    cotizacion = get_object_or_404(OrdenCompra, ID=id)
    cotizacion.estado = 'Denegado'
    cotizacion.save()
    messages.success(request, 'Cotización denegada con éxito.')
    return redirect(reverse('gestionar_cotizaciones'))

def editar_cotizacion(request, id):
    cotizacion = get_object_or_404(OrdenCompra, ID=id)
    if cotizacion.estado != 'Aceptado':  # Permitir la edición si no está aceptada
        if request.method == 'POST':
            form = OrdenCompraForm(request.POST, instance=cotizacion)
            formset = DetalleOrdenFormSet(request.POST, instance=cotizacion)
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                messages.success(request, 'Cotización actualizada con éxito.')
                return redirect('gestionar_cotizaciones')
        else:
            form = OrdenCompraForm(instance=cotizacion)
            formset = DetalleOrdenFormSet(instance=cotizacion)
        return render(request, 'editar_cotizacion.html', {'form': form, 'formset': formset, 'cotizacion': cotizacion})
    else:
        messages.error(request, 'No se puede editar una cotización aceptada.')
        return redirect('gestionar_cotizaciones')
