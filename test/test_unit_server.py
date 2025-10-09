import pytest
from src.server import validar_mensaje, eliminar_cliente


class TestServidor:
    def test_rechazar_mensaje_vacio(self):
        assert validar_mensaje("") is False

    def test_rechaza_mensaje_muy_largo(self):
        mensaje = "x" * 1001
        assert validar_mensaje(mensaje) is False

    def test_aceptar_mensaej_valid(self):
        assert validar_mensaje("Hola mundo") is True

    def test_eliminar_cliente_no_lanza_errores(self):
        class MockCliente:
            def close(self):
                pass

        conn = MockCliente()
        try:
            eliminar_cliente(conn)
        except Exception as e:
            pytest.fail(f"No deberia lanzar excepcion: {e}")
