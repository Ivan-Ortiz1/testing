import socket
import threading


class Cliente:
    def __init__(self, nombre_usuario, host="127.0.0.1", puerto=5555):
        self.nombre_usuario = nombre_usuario
        self.host = host
        self.puerto = puerto
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ultimo_mensaje = None
        self.ejecutando = False

    def conectar(self):
        self.socket.connect((self.host, self.puerto))
        self.ejecutando = True
        threading.Thread(target=self.recibir_mensajes, daemon=True).start()

    def enviar_mensaje(self, mensaje):
        try:
            self.socket.send(mensaje.encode("utf-8"))
        except Exception as e:
            print("Error al enviar mensaje:", e)

    def recibir_mensajes(self):
        while self.ejecutando:
            try:
                msg = self.socket.recv(1024).decode("utf-8")
                if msg:
                    self.ultimo_mensaje = msg
                    print(msg)
            except:
                self.ejecutando = False
                break

    def desconectar(self):
        self.ejecutando = False
        try:
            self.socket.close()
        except:
            pass
