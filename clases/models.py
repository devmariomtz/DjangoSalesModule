import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Sum
from django_countries.fields import CountryField


class Usuario(models.Model):
    ID = models.CharField(
        max_length=4,
        primary_key=True,
        validators=[
            RegexValidator(
                regex="^[GE][0-9]{3}$",
                message="El ID debe comenzar con G o E seguido de 3 números.",
            )
        ],
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    contrasena = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex="^.{4,10}$",
                message="La contraseña debe tener entre 4 y 10 caracteres.",
            )
        ],
    )
    GERENTE = "Gerente"
    EMPLEADO = "Empleado"
    ROL_CHOICES = [
        (GERENTE, "Gerente"),
        (EMPLEADO, "Empleado"),
    ]
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Proveedor(models.Model):
    ID = models.CharField(
        max_length=5,
        primary_key=True,
        validators=[
            RegexValidator(
                regex="^P[0-9]{4}$",
                message="El ID del proveedor debe comenzar con P seguido de 4 dígitos.",
            )
        ],
    )
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex="^\+?[\d-]{1,15}$", message="Número de teléfono inválido."
            )
        ]
    )
    correo_electronico = models.EmailField()
    ciudad = models.CharField(max_length=100)
    pais = CountryField()
    direccion = models.CharField(max_length=255, default="Desconocido")
    tipo_servicio = models.CharField(max_length=100)
    vendedor_nombre = models.CharField(max_length=100)
    vendedor_apellido = models.CharField(max_length=100)
    vendedor_puesto = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    ID = models.CharField(
        max_length=6,
        primary_key=True,
        validators=[
            RegexValidator(
                regex="^[A-Za-z0-9]{1,6}$",
                message="El ID debe tener hasta 6 caracteres, incluyendo letras y números.",
            )
        ],
    )
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100)
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, related_name="productos"
    )

    def __str__(self):
        return self.nombre


class OrdenCompra(models.Model):
    ID = models.CharField(
        max_length=5,
        primary_key=True,
        validators=[
            RegexValidator(
                regex="^C[0-9]{4}$",
                message="El ID de la orden debe comenzar con C seguido de 4 dígitos.",
            )
        ],
        unique=True,
    )
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_limite = models.DateField()
    plazo_pago = models.CharField(max_length=20, default="30 días")
    ENVIADO = "Enviado"
    ACEPTADO = "Aceptado"
    RECHAZADO = "Rechazado"
    ESTADO_CHOICES = [
        (ENVIADO, "Enviado"),
        (ACEPTADO, "Aceptado"),
        (RECHAZADO, "Rechazado"),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default=ENVIADO)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, related_name="ordenes"
    )

    def calcular_total(self):
        total = self.detalles.aggregate(total=Sum("subtotal"))["total"]
        self.total = total if total else 100
        self.save()

    def save(self, *args, **kwargs):
        if not self.ID:
            self.ID = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        while True:
            new_id = f"C{uuid.uuid4().hex[:4].upper()}"
            if not OrdenCompra.objects.filter(ID=new_id).exists():
                return new_id

    # def __str__(self):
    #     return f"Orden #{self.ID} - {self.proveedor.nombre}"


class DetalleOrden(models.Model):
    # orden = models.ForeignKey(
    #     OrdenCompra, on_delete=models.CASCADE, related_name="detalles"
    # )
    # producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    # cantidad = models.IntegerField()
    # precio_unitario = models.DecimalField(
    #     max_digits=10, decimal_places=2, editable=False
    # )

    orden = models.ForeignKey(
        OrdenCompra, 
        on_delete=models.CASCADE, 
        related_name='detalles_orden'
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    # def __str__(self):
    #     return f"{self.producto.nombre} - {self.cantidad} unidades"

    # def save(self, *args, **kwargs):
    #     self.precio_unitario = self.producto.precio
    #     self.subtotal = self.cantidad * self.precio_unitario
    #     super().save(*args, **kwargs)


class productosDetalleOrden(models.Model):
    orden = models.ForeignKey(
        OrdenCompra, 
        on_delete=models.CASCADE, 
        related_name='productos_detalle_orden'
    )
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"

    def save(self, *args, **kwargs):
        self.precio_unitario = self.producto.precio
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)