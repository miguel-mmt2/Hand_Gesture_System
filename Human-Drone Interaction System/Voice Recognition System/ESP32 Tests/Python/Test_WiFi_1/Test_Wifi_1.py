'''
This code was developed by:
    - Miguel Meireles Teixeira, nº 2021217493
    - Damir Ferreira Baspayev Marques, nº 2021218858

Objective: Initial Test on WiFi connection between PC and ESP32.

          This code waits the computer to send a message to ESP32. To receive the message
          we used the code avilable on our GitHub:

This code is available on Github: https://github.com/miguel-mmt2/PL5_Team_1_Repository
'''

# Required Libraries
import socket

# ESP32 WiFi IP
ESP32_IP = '192.168.1.215'  
ESP32_PORT = 80

# Mensagem to send
message = "Hi, ESP32!"

# Socket TCP/IP criation
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # ESP32 connection
    client_socket.connect((ESP32_IP, ESP32_PORT))
    print("Conectado ao servidor ESP32")

    # Send Message to ESP32
    client_socket.sendall(message.encode())
    print("Mensagem enviada com sucesso")

except Exception as e:
    print("Ocorreu um erro:", e)

