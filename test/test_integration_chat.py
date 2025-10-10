import threading
import time
from src.server import iniciar_servidor
from src.client import Cliente


class TestChatIntegracion:

    def test_multiples_clientes_reciben_mensajes(self):
        servidor_thread = threading.Thread(target=iniciar_servidor, daemon=True)
        servidor_thread.start()
        time.sleep(0.5)

        cliente1 = Cliente("User1")
        cliente2 = Cliente("User2")

        cliente1.conectar()
        cliente2.conectar()

        cliente1.enviar_mensaje("Hola desde User1")
        time.sleep(0.5)

        assert "Hola desde User1" in cliente2.ultimo_mensaje

        cliente1.desconectar()
        cliente2.desconectar()

    def test_desconexion_no_afecta_a_otros(self):
        servidor_thread = threading.Thread(target=iniciar_servidor, daemon=True)
        servidor_thread.start()
        time.sleep(0.5)

        cliente1 = Cliente("User1")
        cliente2 = Cliente("User2")
        cliente1.conectar()
        cliente2.conectar()

        cliente1.enviar_mensaje("Mensaje antes de desconexión")
        cliente1.desconectar()
        time.sleep(0.5)

        cliente2.enviar_mensaje("Mensaje después de desconexión")
        time.sleep(0.5)

        assert "Mensaje después" in (cliente2.ultimo_mensaje or "")
        cliente2.desconectar()
