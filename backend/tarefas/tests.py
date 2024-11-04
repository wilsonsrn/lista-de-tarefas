from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Tarefa
from django.urls import reverse


class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tarefa_url = reverse("tarefa-list")

    def test_create_tarefa(self):
        """
        Teste para criação de uma tarefa.
        """
        payload = {
            "nome": "Teste de Tarefa",
            "custo": "500.00",
            "data_limite": "2024-12-31",
            "ordem": Tarefa.objects.count() + 1,
        }
        response = self.client.post(self.tarefa_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tarefa.objects.count(), 1)
        self.assertEqual(Tarefa.objects.get().nome, "Teste de Tarefa")

    def test_create_tarefa_com_nome_duplicado(self):
        """
        Teste para garantir que uma tarefa com nome duplicado não seja criada.
        """
        Tarefa.objects.create(
            nome="Duplicada", custo=100, data_limite="2024-12-31", ordem=1
        )
        payload = {
            "nome": "Duplicada",
            "custo": "500.00",
            "data_limite": "2024-12-31",
            "ordem": Tarefa.objects.count() + 1,
        }
        response = self.client.post(self.tarefa_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_lista_tarefas(self):
        """
        Teste para listar as tarefas e garantir a ordem.
        """
        Tarefa.objects.create(
            nome="Tarefa A",
            custo=200,
            data_limite="2024-12-31",
            ordem=Tarefa.objects.count() + 1,
        )
        Tarefa.objects.create(
            nome="Tarefa B",
            custo=1500,
            data_limite="2024-12-31",
            ordem=Tarefa.objects.count() + 1,
        )
        response = self.client.get(self.tarefa_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["nome"], "Tarefa A")
        self.assertEqual(response.data[1]["nome"], "Tarefa B")

    def test_mostra_tarefas_custo_alto(self):
        """
        Teste para verificar que tarefas com custo >= 1000 são destacadas.
        """
        Tarefa.objects.create(
            nome="Tarefa C",
            custo=1200,
            data_limite="2024-12-31",
            ordem=Tarefa.objects.count() + 1,
        )
        response = self.client.get(self.tarefa_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["custo"], "1200.00")

    def test_update_tarefa(self):
        """
        Teste para atualizar uma tarefa e garantir exclusividade do nome.
        """
        tarefa = Tarefa.objects.create(
            nome="Tarefa Atualizar",
            custo=100,
            data_limite="2024-12-31",
            ordem=Tarefa.objects.count() + 1,
        )
        payload = {
            "nome": "Tarefa Atualizada",
            "custo": "600.00",
            "data_limite": "2024-12-31",
            "ordem": Tarefa.objects.count(),
        }
        response = self.client.put(
            reverse("tarefa-detail", args=[tarefa.id]), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tarefa.refresh_from_db()
        self.assertEqual(tarefa.nome, "Tarefa Atualizada")

    def test_delete_tarefa(self):
        """
        Teste para excluir uma tarefa.
        """
        tarefa = Tarefa.objects.create(
            nome="Tarefa Excluir", custo=300, data_limite="2024-12-31", ordem=1
        )
        response = self.client.delete(reverse("tarefa-detail", args=[tarefa.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tarefa.objects.count(), 0)
