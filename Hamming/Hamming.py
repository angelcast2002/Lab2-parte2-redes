import math
import socket
import random
import matplotlib.pyplot as plt

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
    #seleccionar x (tasa de error) bits aleatorios y cambiarlos
    n = len(mensaje)
    if tasa_error == 0:
        return mensaje
    if tasa_error == 1:
        # Cambiar un bit aleatorio
        bit = random.randint(0, n - 1)
        mensaje[bit] = '0' if mensaje[bit] == '1' else '1'
        print(f"Se cambió el bit {bit} a {mensaje[bit]}")
        return mensaje
    for i in range(len(mensaje)):
        if random.random() < tasa_error / 1000:
            mensaje[i] = '0' if mensaje[i] == '1' else '1'
    return mensaje

def mensaje_a_binario(mensaje):
    return ''.join(format(ord(c), '08b') for c in mensaje)

def main():
    mensajes = ["Hola", "Mundo", "Como", "Estas", "Hoy", "Es", "Un", "Buen", "Dia", "Para", "Aprender", "Sobre", "Redes", "De", "Computadoras", "Y", "Comunicaciones"]
    probabilidades_prueba_1 = [5, 10, 15, 20, 25, 30, 25, 20, 15, 10, 5, 10, 15, 20, 25, 30, 80]
    probabilidades_prueba_2 = [1] * 17
    probabilidades_prueba_3 = [0] * 17
    mensajes_recibidos = []
    mensajes_correctos_1 = []
    mensajes_correctos_2 = []
    mensajes_correctos_3 = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 65432))
        for mensaje, tasa_error in zip(mensajes, probabilidades_prueba_1):
            print("-" * 50)
            print(f"Mensaje seleccionado: {mensaje} con tasa de error: {tasa_error}%")
            mensaje_binario = list(mensaje_a_binario(mensaje))
            mensaje_codificado = hamming(mensaje_binario)
            print(f"Mensaje codificado: {''.join(mensaje_codificado)}")
            mensaje_con_ruido = aplicar_ruido(mensaje_codificado.copy(), tasa_error)
            print(f"Mensaje con ruido: {''.join(mensaje_con_ruido)}")
            mensaje_final = ''.join(mensaje_con_ruido)
            s.sendall(mensaje_final.encode())
            print(f"Mensaje enviado: {mensaje_final}")
            
            #input("Presione Enter para enviar el siguiente mensaje...")

            # Recibimos la respuesta del servidor
            data = s.recv(1024)
            mensajes_recibidos.append(data.decode())
    
    #comparar mensajes
    for mensaje, mensaje_recibido in zip(mensajes, mensajes_recibidos):
        if mensaje == mensaje_recibido:
            mensajes_correctos_1.append(1)
    mensajes_recibidos = []

    #calcular porcentaje de mensajes correctos
    porcentaje_1 = len(mensajes_correctos_1) / len(mensajes) * 100
    print("-" * 50)
    print(f"Porcentaje de mensajes correctos: {porcentaje_1}%")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 65432))
        for mensaje, tasa_error in zip(mensajes, probabilidades_prueba_2):
            print("-" * 50)
            print(f"Mensaje seleccionado: {mensaje} con tasa de error: {tasa_error}%")
            mensaje_binario = list(mensaje_a_binario(mensaje))
            mensaje_codificado = hamming(mensaje_binario)
            print(f"Mensaje codificado: {''.join(mensaje_codificado)}")
            mensaje_con_ruido = aplicar_ruido(mensaje_codificado.copy(), tasa_error)
            print(f"Mensaje con ruido: {''.join(mensaje_con_ruido)}")
            mensaje_final = ''.join(mensaje_con_ruido)
            s.sendall(mensaje_final.encode())
            print(f"Mensaje enviado: {mensaje_final}")
            
            #input("Presione Enter para enviar el siguiente mensaje...")

            # Recibimos la respuesta del servidor
            data = s.recv(1024)
            mensajes_recibidos.append(data.decode())
    
    #comparar mensajes
    for mensaje, mensaje_recibido in zip(mensajes, mensajes_recibidos):
        if mensaje == mensaje_recibido:
            mensajes_correctos_2.append(1)
    mensajes_recibidos = []

    #calcular porcentaje de mensajes correctos
    porcentaje_2 = len(mensajes_correctos_2) / len(mensajes) * 100
    print("-" * 50)
    print(f"Porcentaje de mensajes correctos: {porcentaje_2}%")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 65432))
        for mensaje, tasa_error in zip(mensajes, probabilidades_prueba_3):
            print("-" * 50)
            print(f"Mensaje seleccionado: {mensaje} con tasa de error: {tasa_error}%")
            mensaje_binario = list(mensaje_a_binario(mensaje))
            mensaje_codificado = hamming(mensaje_binario)
            print(f"Mensaje codificado: {''.join(mensaje_codificado)}")
            mensaje_con_ruido = aplicar_ruido(mensaje_codificado.copy(), tasa_error)
            print(f"Mensaje con ruido: {''.join(mensaje_con_ruido)}")
            mensaje_final = ''.join(mensaje_con_ruido)
            s.sendall(mensaje_final.encode())
            print(f"Mensaje enviado: {mensaje_final}")
            
            #input("Presione Enter para enviar el siguiente mensaje...")

            # Recibimos la respuesta del servidor
            data = s.recv(1024)
            mensajes_recibidos.append(data.decode())
    
    #comparar mensajes
    for mensaje, mensaje_recibido in zip(mensajes, mensajes_recibidos):
        if mensaje == mensaje_recibido:
            mensajes_correctos_3.append(1)
    mensajes_recibidos = []

    #calcular porcentaje de mensajes correctos
    porcentaje_3 = len(mensajes_correctos_3) / len(mensajes) * 100
    print("-" * 50)
    print(f"Porcentaje de mensajes correctos: {porcentaje_3}%")

            
    # Graficar los resultados
    categorias = ['Prueba 1 (probabilidad de >1 error)', 'Prueba 2 (1 error)', 'Prueba 3 (sin error)']
    valores = [porcentaje_1, porcentaje_2, porcentaje_3]

    plt.bar(categorias, valores, color=['red', 'green', 'blue'])
    plt.xlabel('Pruebas')
    plt.ylabel('Porcentaje de Mensajes Correctos')
    plt.title('Resultados de las Pruebas de Comunicación')
    plt.show()


if __name__ == "__main__":
    main()

