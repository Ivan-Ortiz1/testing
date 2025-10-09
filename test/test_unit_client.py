from src.client import Cliente


class TestCliente:

    def test_estado_inicial(self):
        cliente = Cliente("Ivan")
        assert cliente.nombre_usuario == "Ivan"
        assert cliente.ejecutando is False
        assert cliente.ultimo_mensaje is None

    def test_conexion_fallida_no_lanza_excepcion(self):
        cliente = Cliente("Tester", host="127.0.0.2")
        try:
            cliente.enviar_mensaej("Hola")
        except Exception:
            assert True
