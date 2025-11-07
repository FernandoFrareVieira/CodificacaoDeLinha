import socket

HOST = '0.0.0.0' 
PORTA = 12345

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, PORTA))
socket.listen(1)
print(f"Servidor 'dummy' ouvindo na porta {PORTA}...")

while True:
    conn, addr = socket.accept()
    print(f"Conexão recebida de {addr}")
    conn.close()