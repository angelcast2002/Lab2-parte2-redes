import math
import socket
import random

def calcular_bits_paridad(mensaje, r):
    bp_pos = []
    for i in range(r):
        posicion = int(math.pow(2, i))
        mensaje.insert(posicion - 1, '0')
        bp_pos.append(posicion)
    return bp_pos

def actualizar_bits_paridad(mensaje, bp_pos):
    for posicion in bp_pos:
        contador = 0
        for j in range(1, len(mensaje) + 1):
            if j & posicion == posicion and mensaje[j - 1] == '1':
                contador += 1
        mensaje[posicion - 1] = '0' if contador % 2 == 0 else '1'

def hamming(mensaje):
    mensaje = mensaje[::-1]
    m = len(mensaje)
    r = 0
    while math.pow(2, r) < m + r + 1:
        r += 1
    bp_pos = calcular_bits_paridad(mensaje, r)
    actualizar_bits_paridad(mensaje, bp_pos)
    return mensaje[::-1]

def aplicar_ruido(mensaje, tasa_error):
    for i in range(len(mensaje)):
        if random.random() < tasa_error / 100:  # Convertimos la tasa de error a porcentaje
            mensaje[i] = '0' if mensaje[i] == '1' else '1'
            print(f"Bit {i + 1} alterado")
            return mensaje
    return mensaje

def mensaje_a_binario(mensaje):
    return ''.join(format(ord(c), '08b') for c in mensaje)

def main():
    mensajes = ["Hola", "Mundo", "Como", "Estas", "Hoy", "Es", "Un", "Buen", "Dia", "Para", "Aprender", "Sobre", "Redes", "De", "Computadoras", "Y", "Comunicaciones"]
    probabilidades = [5, 10, 15, 20, 25, 30, 25, 20, 15, 10, 5, 10, 15, 20, 25, 30, 80]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 65432))
        for mensaje, tasa_error in zip(mensajes, probabilidades):
            print(f"Mensaje seleccionado: {mensaje} con tasa de error: {tasa_error}%")
            mensaje_binario = list(mensaje_a_binario(mensaje))
            mensaje_codificado = hamming(mensaje_binario)
            print(f"Mensaje codificado: {''.join(mensaje_codificado)}")
            mensaje_con_ruido = aplicar_ruido(mensaje_codificado.copy(), tasa_error)
            print(f"Mensaje con ruido: {''.join(mensaje_con_ruido)}")
            mensaje_final = ''.join(mensaje_con_ruido)
            s.sendall(mensaje_final.encode())
            print(f"Mensaje enviado: {mensaje_final}")
            
            input("Presione Enter para enviar el siguiente mensaje...")

if __name__ == "__main__":
    main()

