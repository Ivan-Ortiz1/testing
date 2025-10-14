import pytest
from src.client import Cliente


class TestCliente:

    def test_estado_inicial(self):
        cliente = Cliente("Ivan")
        assert cliente.nombre_usuario == "Ivan"
        assert cliente.ejecutando is False
        assert cliente.ultimo_mensaje is None

    def test_conexion_fallida_no_lanza_excepcion(self):
        cliente = Cliente("Tester", host="127.0.0.2")
        # Intentar enviar sin conexión no debe propagar una excepción
        try:
            cliente.enviar_mensaje("Hola")
        except Exception as e:
            pytest.fail(f"No debería lanzar excepción: {e}")
