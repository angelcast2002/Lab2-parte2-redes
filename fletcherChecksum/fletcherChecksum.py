import random
import socket
import time

HOST = 'localhost'
PORT = 9000

def fletcher16(mensaje):
    mensajeBytes = []
    
    for i in range(0, len(mensaje), 8):
        byte_str = mensaje[i:i+8]
        byte = int(byte_str, 2)
        mensajeBytes.append(byte)
    
    sum1 = 0
    sum2 = 0
    for byte in mensajeBytes:
        sum1 = (sum1 + byte) % 255
        sum2 = (sum2 + sum1) % 255
    return (sum2 << 8) | sum1

def covertidorBinario(mensaje):
    mensajeBinario = ""
    for i in range(len(mensaje)):
        mensajeBinario += format(ord(mensaje[i]), '08b')
    return mensajeBinario

def ruido(mensaje, probabilidad):
    mensajeRuidoso = ""
    for bit in mensaje:
        if random.random() < probabilidad:
            mensajeRuidoso += str(1 - int(bit))  # Flip the bit
        else:
            mensajeRuidoso += bit
    return mensajeRuidoso

def comunicarMensaje(mensaje):
    try:
        Csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Csocket.connect((HOST, PORT))
        Csocket.sendall(mensaje.encode())
        print("Mensaje enviado con éxito.")
        # time.sleep(2)
    except Exception as e:
        print(f"Error al comunicar el mensaje: {e}")
    finally:
        Csocket.close()
    

def main():
    # mensaje = "1100001110110001"
    mensaje = input("Ingrese el mensaje a enviar: ")
    probabilidad = int(input("Ingrese la probabilidad de ruido (0 - 100): "))
    probabilidad = probabilidad / 100
    mensaje = covertidorBinario(mensaje)
    print("Mensaje en binario: ", mensaje)

    checksum = fletcher16(mensaje)

    checksumBinario = format(checksum, '016b')
    # print("Checksum: ", checksumBinario)
    mensajeAEnviar = mensaje + checksumBinario
    mensajeAEnviar = ruido(mensajeAEnviar, probabilidad)
    comunicarMensaje(mensajeAEnviar)
    print("Mensaje a enviar: ", mensajeAEnviar)


if __name__ == "__main__":
    main()
