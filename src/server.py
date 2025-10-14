import socket
import threading

clientes = []


def validar_mensaje(mensaje: str) -> bool:
    """Valida que el mensaje no esté vacío ni sea demasiado largo."""
    return bool(mensaje.strip()) and len(mensaje) <= 1000


def eliminar_cliente(conn):
    """Eliminar y cerrar conexión."""
    if conn in clientes:
        clientes.remove(conn)
    try:
        conn.close()
    except:
        pass


class ChatServer:
    """Servidor encapsulado: acepta conexiones y difunde mensajes."""

    def __init__(self, host="127.0.0.1", puerto=5555, backlog=5, timeout=0.5):
        self.host = host
        self.puerto = puerto
        self.backlog = backlog
        self.timeout = timeout
        self._sock = None
        self._running = False

    def _difundir(self, mensaje: str, remitente=None):
        for cliente in list(clientes):
            if cliente is remitente:
                continue
            try:
                cliente.send(mensaje.encode("utf-8"))
            except:
                eliminar_cliente(cliente)

    def _manejar_cliente(self, conn, addr):
        print(f"Cliente conectado: {addr}")
        while True:
            try:
                msg = conn.recv(1024).decode("utf-8")
                if not msg or not validar_mensaje(msg):
                    continue
                self._difundir(msg, conn)
            except:
                eliminar_cliente(conn)
                break

    def start(self, stop_event: threading.Event = None):
        """Arranca el servidor; si se pasa stop_event, se detiene al setearlo."""
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, self.puerto))
        self._sock.listen(self.backlog)
        self._sock.settimeout(self.timeout)
        self._running = True
        print(f"Servidor escuchando en {self.host}:{self.puerto}")

        try:
            if stop_event is None:
                while True:
                    try:
                        conn, addr = self._sock.accept()
                    except socket.timeout:
                        continue
                    clientes.append(conn)
                    hilo = threading.Thread(
                        target=self._manejar_cliente, args=(conn, addr), daemon=True
                    )
                    hilo.start()
            else:
                while not stop_event.is_set():
                    try:
                        conn, addr = self._sock.accept()
                    except socket.timeout:
                        continue
                    clientes.append(conn)
                    hilo = threading.Thread(
                        target=self._manejar_cliente, args=(conn, addr), daemon=True
                    )
                    hilo.start()
        finally:
            # cerrar conexiones y socket
            for c in list(clientes):
                try:
                    c.close()
                except:
                    pass
            try:
                if self._sock:
                    self._sock.close()
            except:
                pass
            self._running = False


def iniciar_servidor(host="127.0.0.1", puerto=5555, stop_event: threading.Event = None):
    """Compatibilidad: función que inicia un ChatServer."""
    servidor = ChatServer(host, puerto)
    servidor.start(stop_event)
