from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Tarefa
from .serializers import TarefaSerializer


class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all().order_by("ordem")
    serializer_class = TarefaSerializer

    def create(self, request, *args, **kwargs):
        nome = request.data.get("nome")
        if Tarefa.objects.filter(nome=nome).exists():
            return Response(
                {"error": "Nome da tarefa precisa ser única"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        nome = request.data.get("nome")
        if Tarefa.objects.filter(nome=nome).exclude(id=kwargs["pk"]).exists():
            return Response(
                {"error": "Nome da tarefa precisa ser única"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().update(request, *args, **kwargs)
