from django.db import models


class Tarefa(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    data_limite = models.DateField()
    ordem = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return self.nome
