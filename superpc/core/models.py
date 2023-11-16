from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from core.templatetags.custom_filters import formatear_dinero

from django.db import models
from django.db.models import Min
from django.db import connection

# Modelos categoria

class Usuario(models.Model):
    idUsuario = models.IntegerField(primary_key=True, verbose_name='Id de Usuario')
    nombreUsuario = models.CharField(max_length=120, blank=False, null=False, verbose_name='Nombre de Usuario')

    def __str__(self):
        return self.nombreUsuario


# Modelos productos


class Perfil(models.Model):
    USUARIO_CHOICES = [
        ('Cliente', 'cliente'),
        ('Administrador', 'Administrador'),
        ('Superusuario', 'Superusuario'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(
        choices=USUARIO_CHOICES,
        max_length=50,
        blank=False,
        null=False,
        verbose_name='Tipo de usuario'
    )
    rut = models.CharField(max_length=15, blank=False, null=False, verbose_name='Rut')
    Direccion = models.CharField(max_length=400, blank=False, null=False, verbose_name='Direccion')
    Telefono = models.IntegerField(blank=False, null=False, verbose_name='Telefono')

    class Meta:
        db_table = 'Perfil'
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuarios'
        ordering = ['Tipo_usuario']

    def __str__(self):
        if self.tipo_usuario == 'Cliente':
            return f'{self.usuario.first_name} {self.usuario.last_name} (ID {self.id} - {self.tipo_usuario})'

    def acciones():
        return{ 
            'accion_eliminar': 'eliminar el Perfil',
            'accion_actualizar': 'actualizar el Perfil'
        }
    

    class Boleta(models.Model):
        ESTADO_CHOICES = [
            ('Anulado', 'Anulado'),
            ('Atendido', 'Atendido'),
            ('Pendiente', 'Pendiente'),
        ]
    nro_boleta = models.IntegerField(primary_key=True, blank=False, null=False, verbose_name='Nro boleta')
    cliente = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING) # ->  FR No entiendo porque no detecta el perfil, capaz toca arreglarlo
    monto_sin_iva = models.IntegerField(blank=False, null=False, verbose_name='Monto sin IVA')
    iva = models.IntegerField(blank=False, null=False, verbose_name='IVA')
    total_a_pagar = models.IntegerField(blank=False, null=False, verbose_name='Total a pagar')
    fecha_atencion = models.DateField(blank=False, null=False, verbose_name='Fecha de atencion')
    estado = models.CharField(choices=ESTADO_CHOICES, max_length=50, blank=False, null=False, verbose_name='Estado')

    class Meta:
        db_table = 'Boleta'
        verbose_name = 'Boleta'
        verbose_name_plural = 'Boletas'

    def __str__(self):
        return f'Boleta {self.nro_boleta} de {self.cliente.usuario.first_name} {self.cliente.usuario.last_name} por {formatear_dinero(self.total_a_pagar)}'
    
    def acciones():
        return {
            'accion_eliminar': 'eliminar la Boleta',
            'accion_actualizar': 'actualizar la Boleta'
        }

    class DetalleBoleta(models.Model):
        boleta = models.ForeignKey(Boleta, on_delete=models.DO_NOTHING)
        precio = models.IntegerField(blank=False, null=False, verbose_name='Precio')
        precio_a_pagar = models.IntegerField(blank=False, null=False, verbose_name='Precio a pagar')


    class Meta:
        db_table = 'DetalleBoleta'
        verbose_name = 'Detalle de Boleta'
        verbose_name_plural = 'Detalles de Boletas'

    def __str__(self):
        return f'Detalle de la Boleta {self.boleta.nro_boleta} - {formatear_dinero(self.precio_a_pagar)}'
    
    def acciones():
        return {
            'accion_eliminar': 'eliminar el Detalle de la Boleta',
            'accion_actualizar': 'actualizar el Detalle de la Boleta'
        }
        