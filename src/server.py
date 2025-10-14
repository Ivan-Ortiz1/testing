import socket
import threading

clientes = []


def validar_mensaje(mensaje: str) -> bool:
    """Valida que el mensaje no esté vacío ni sea demasiado largo."""
    return bool(mensaje.strip()) and len(mensaje) <= 1000


def difundir_mensaje(mensaje: str, remitente=None):
    """Envía un mensaje a todos los clientes conectados, excepto al remitente."""
    for cliente in clientes:
        if cliente != remitente:
            try:
                cliente.send(mensaje.encode("utf-8"))
            except:
                eliminar_cliente(cliente)


def manejar_cliente(conn, addr):
    """Maneja la comunicación con un cliente."""
    print(f"Cliente conectado: {addr}")
    while True:
        try:
            msg = conn.recv(1024).decode("utf-8")
            if not msg or not validar_mensaje(msg):
                continue
            difundir_mensaje(msg, conn)
        except:
            eliminar_cliente(conn)
            break


def eliminar_cliente(conn):
    """Elimina un cliente de la lista y cierra su conexión."""
    if conn in clientes:
        clientes.remove(conn)
    try:
        conn.close()
    except:
        pass


def iniciar_servidor(host="127.0.0.1", puerto=5555, stop_event: threading.Event = None):
    """Inicia el servidor y escucha múltiples conexiones.
    Si se pasa stop_event, el servidor se detendrá cuando se establezca ese Event."""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((host, puerto))
    servidor.listen()
    servidor.settimeout(0.5)  # permite comprobar periódicamente stop_event
    print(f"Servidor escuchando en {host}:{puerto}")

    try:
        if stop_event is None:
            # comportamiento legacy: bucle infinito
            while True:
                try:
                    conn, addr = servidor.accept()
                except socket.timeout:
                    continue
                clientes.append(conn)
                hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
                hilo.start()
        else:
            while not stop_event.is_set():
                try:
                    conn, addr = servidor.accept()
                except socket.timeout:
                    continue
                clientes.append(conn)
                hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
                hilo.start()
    finally:
        # cerrar todas las conexiones cliente y el socket del servidor
        for c in list(clientes):
            try:
                c.close()
            except:
                pass
        try:
            servidor.close()
        except:
            pass
