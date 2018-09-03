from django.db import models

class Alimento(models.Model):
    nombre = models.CharField(max_length=200)
    unidad = models.DecimalField(max_digits=20, decimal_places=10)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    calorias = models.DecimalField(max_digits=20, decimal_places=10)
    proteinas = models.DecimalField(max_digits=20, decimal_places=10)
    calcio = models.DecimalField(max_digits=20, decimal_places=10)
    hierro = models.DecimalField(max_digits=20, decimal_places=10)
    vitamina_a = models.DecimalField(max_digits=20, decimal_places=10)
    vitamina_b1 = models.DecimalField(max_digits=20, decimal_places=10)
    vitamina_b2 = models.DecimalField(max_digits=20, decimal_places=10)
    vitamina_b3 = models.DecimalField(max_digits=20, decimal_places=10)
    vitamina_c = models.DecimalField(max_digits=20, decimal_places=10)

    def __str__(self):
        return self.nombre


class Cantidad(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=10)

    def __str__(self):
        return str(self.alimento) + ' (' + str(self.cantidad) + ')'


class Comida(models.Model):
    alimentos = models.ManyToManyField(Cantidad)
    es_desayuno = models.BooleanField(default=True)
    es_almuerzo = models.BooleanField(default=True)
    es_comida = models.BooleanField(default=True)
    es_merienda = models.BooleanField(default=True)
    es_cena = models.BooleanField(default=True)

    def __str__(self):
        return ', '.join([str(alimento) for alimento in self.alimentos.all()])
