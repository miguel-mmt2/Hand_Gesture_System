import socket

# Endereço IP do ESP32 e porta em que está escutando
ESP32_IP = '172.20.10.7'  # Substitua pelo endereço IP do seu ESP32
ESP32_PORT = 80

# Mensagem a ser enviada
message = "Olá, ESP32!"

# Criação do socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conexão com o ESP32
    client_socket.connect((ESP32_IP, ESP32_PORT))
    print("Conectado ao servidor ESP32")

    # Envio da mensagem
    client_socket.sendall(message.encode())
    print("Mensagem enviada com sucesso")

    # Recebimento da resposta do servidor
    data = client_socket.recv(1024)
    print("Resposta do servidor:", data.decode())

except Exception as e:
    print("Ocorreu um erro:", e)

    # Fechamento do socket
    client_socket.close()
