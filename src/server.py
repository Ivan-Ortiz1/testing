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


def iniciar_servidor(host="127.0.0.1", puerto=5555):
    """Inicia el servidor y escucha múltiples conexiones."""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen()
    print(f"Servidor escuchando en {host}:{puerto}")

    while True:
        conn, addr = servidor.accept()
        clientes.append(conn)
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
        hilo.start()
