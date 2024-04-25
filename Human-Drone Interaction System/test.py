import serial.tools.list_ports

# Listar as portas seriais disponíveis
ports = serial.tools.list_ports.comports()
portsList = [str(onePort) for onePort in ports]
print("Available ports:")
for port in portsList:
    print(port)

# Selecionar a porta serial
portVar = '/dev/cu.usbmodem1101'

# Configurar a porta serial
serialInst = serial.Serial(port=portVar, baudrate=9600)
# serialInst.open()

# # Limpar o buffer serial 
# serialInst.reset_input_buffer()
# serialInst.reset_output_buffer()

# Loop principal
while True:
    if serialInst.in_waiting:
        # Lê uma linha da porta serial
        packet = serialInst.readline().decode().strip()
        print(packet)
        
        # Verifica se a linha lida é igual a 'VERDEEEEE'
        if packet == 'GREEN':
            print("Received ON")
 #           drone.takeoff()

        elif packet == 'RED':
            print("Received OFF")
#            drone.land()
