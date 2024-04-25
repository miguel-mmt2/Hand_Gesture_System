'''
This code was developed by:
    - Miguel Meireles Teixeira, nº 2021217493
    - Damir Ferreira Baspayev Marques, nº 2021218858

Objective: Final Code on WiFi connection between PC and ESP32.

          This code waits the computer to send a message to ESP32. To receive the message
          we used the code avilable on our GitHub:

This code is available on Github: https://github.com/miguel-mmt2/PL5_Team_1_Repository
'''

# Required Libraries
import socket
import serial
import serial.tools.list_ports

# ESP32 WiFi IP
ESP32_IP = '192.168.1.215' 
ESP32_PORT = 80

# Socket TCP/IP criation
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # ESP32 connection
    client_socket.connect((ESP32_IP, ESP32_PORT))
    print("Conectado ao servidor ESP32")

    # Serial Ports available
    ports = serial.tools.list_ports.comports()
    portsList = [str(onePort) for onePort in ports]
    print("Available ports:")
    for port in portsList:
        print(port)

    # Serial port that the Arduino Nano Ble Sense is connected
    portVar = '/dev/cu.usbmodem11101'

    # Serial Port configuration
    serialInst = serial.Serial(port=portVar, baudrate=9600)

    while True:
        if serialInst.in_waiting:
            # Read the Serial Port
            packet = serialInst.readline().decode().strip()
            print(packet)

            # Send Message to ESP32
            if packet == 'GREEN':
                message = "GREEN"
                print("Received GREEN, sending message to ESP32:", message)
                client_socket.sendall(message.encode())

            elif packet == 'RED':
                message = "RED"
                print("Received RED, sending message to ESP32:", message)
                client_socket.sendall(message.encode())

except Exception as e:
    print("Error", e)
