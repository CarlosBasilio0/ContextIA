from django.db import models


class Analisis(models.Model):

    texto = models.TextField()

    resultado = models.TextField(
        blank=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Análisis #{self.id}"