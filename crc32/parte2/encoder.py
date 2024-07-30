import socket
import random
import threading
import queue
import matplotlib.pyplot as plt

def crc32_manual(data):
    crc = 0xFFFFFFFF
    polynomial = 0xEDB88320

    for i in range(0, len(data), 8):
        byte = int(data[i:i+8], 2)
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1

    return crc ^ 0xFFFFFFFF

def data_to_binary(data):
    return ''.join(format(byte, '08b') for byte in data)

def apply_noise(data, probability):
    noisy_data = list(data)
    for i in range(len(noisy_data)):
        if random.random() < probability:
            noisy_data[i] = '1' if noisy_data[i] == '0' else '0'
    return ''.join(noisy_data)

def send_message(sock, addr, message):
    sock.sendto(message.encode(), addr)

def receive_message(sock, response_queue):
    try:
        response, _ = sock.recvfrom(1024)
        response_queue.put(response.decode())
    except socket.timeout:
        response_queue.put("timeout")

def main():
    random.seed(0)
    mensajes = ["Hola", "Mundo", "Como", "Estas", "Hoy", "Es", "Un", "Buen", "Dia", "Para", "Aprender", "Sobre", "Redes", "De", "Computadoras", "Y", "Comunicaciones"]
    probabilidades = [0.0005, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.0025, 0.002, 0.0015, 0.001, 0.0005, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.008]

    valid_count = 0
    invalid_count = 0

    addr = ('localhost', 12345)

    for i, mensaje in enumerate(mensajes):
        binary_str = data_to_binary(mensaje.encode())
        crc = crc32_manual(binary_str)
        crc_binary = format(crc, '032b')
        encoded_msg = binary_str + crc_binary
        noisy_msg = apply_noise(encoded_msg, probabilidades[i])
        print(f"Mensaje original: {mensaje}")
        print(f"Mensaje codificado: {encoded_msg}")
        print(f"Mensaje con ruido: {noisy_msg}")

        # Crear el socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)

        # Cola para las respuestas
        response_queue = queue.Queue()

        # Crear y empezar el hilo para enviar el mensaje
        send_thread = threading.Thread(target=send_message, args=(sock, addr, noisy_msg))
        send_thread.start()

        # Crear y empezar el hilo para recibir la respuesta
        receive_thread = threading.Thread(target=receive_message, args=(sock, response_queue))
        receive_thread.start()

        # Esperar a que los hilos terminen
        send_thread.join()
        receive_thread.join()

        # Procesar la respuesta
        response = response_queue.get()
        if response == "valid":
            valid_count += 1
        elif response == "invalid":
            invalid_count += 1
        else:
            print("No response received or timeout")

        # Cerrar el socket
        sock.close()

    # Generar el gráfico de pastel
    labels = 'Validos', 'No Validos'
    sizes = [valid_count, invalid_count]
    colors = ['#ff9999','#66b3ff']
    explode = (0.1, 0)  # explotar el primer segmento (válidos)

    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # asegura que el gráfico de pastel es un círculo
    plt.title('Porcentaje de Mensajes Validos vs No Validos')
    plt.show()

if __name__ == "__main__":
    main()
