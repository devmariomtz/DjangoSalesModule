from django import forms
from django.core.validators import RegexValidator
from django.forms import inlineformset_factory

from .models import Usuario, Proveedor, Producto, DetalleOrden, OrdenCompra

class LoginForm(forms.Form):
    id = forms.CharField(
        max_length=4,
        min_length=4,
        validators=[
            RegexValidator(
                regex='^[GE][0-9]{3}$',
                message='Formato de ID inválido. El ID debe comenzar con G o E seguido de 3 números.'
            )
        ]
    )
    contrasena = forms.CharField(widget=forms.PasswordInput)

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['ID', 'nombre', 'apellido', 'contrasena', 'rol']

    def clean_ID(self):
        ID = self.cleaned_data['ID']
        if not ID.startswith(('G', 'E')):
            raise forms.ValidationError('El ID debe comenzar con G (Gerente) o E (Empleado).')
        return ID

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['ID', 'nombre', 'precio', 'descripcion', 'categoria', 'proveedor']

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['ID', 'fecha_limite', 'plazo_pago', 'proveedor']
        widgets = {
            'ID': forms.TextInput(attrs={'maxlength': 5, 'pattern': '^C[0-9]{4}$', 'title': 'El ID debe comenzar con C seguido de 4 dígitos.'}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
        }
class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.none()

        if 'proveedor' in self.data:
            try:
                proveedor_id = int(self.data.get('proveedor'))
                self.fields['producto'].queryset = Producto.objects.filter(proveedor_id=proveedor_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  # fallback to empty queryset
        elif self.instance.pk:
            self.fields['producto'].queryset = self.instance.proveedor.producto_set.order_by('nombre')

            def clean(self):
                cleaned_data = super().clean()
                producto_id = cleaned_data.get('producto')
                print("Instancia de DetalleOrden:", self.instance)  # Agregar esta línea
                if not Producto.objects.filter(id=producto_id).exists():
                    raise forms.ValidationError("Producto no válido")
                return cleaned_data

DetalleOrdenFormSet = inlineformset_factory(OrdenCompra, DetalleOrden, form=DetalleOrdenForm, extra=1, can_delete=True)

