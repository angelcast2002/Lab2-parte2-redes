import math

def calcular_bits_paridad(mensaje, r):
    # Inicializamos la lista para guardar las posiciones de los bits de paridad
    bp_pos = []

    # Insertamos los bits de paridad en el mensaje y guardamos sus posiciones
    for i in range(r):
        posicion = int(math.pow(2, i))
        mensaje.insert(posicion - 1, '0')
        bp_pos.append(posicion)

    return bp_pos

def actualizar_bits_paridad(mensaje, bp_pos):
    # Calculamos y actualizamos los bits de paridad en el mensaje
    for posicion in bp_pos:
        contador = 0
        for j in range(1, len(mensaje) + 1):
            if j & posicion == posicion and mensaje[j - 1] == '1':
                contador += 1
        mensaje[posicion - 1] = '0' if contador % 2 == 0 else '1'

def hamming(mensaje):
    mensaje = mensaje[::-1]  # Invertimos el mensaje para facilitar la inserción de bits de paridad
    m = len(mensaje)
    r = 0

    # Calculamos el número de bits de paridad necesarios
    while math.pow(2, r) < m + r + 1:
        r += 1

    bp_pos = calcular_bits_paridad(mensaje, r)  # Calculamos las posiciones de los bits de paridad
    actualizar_bits_paridad(mensaje, bp_pos)    # Actualizamos los bits de paridad en el mensaje

    return mensaje[::-1]  # Devolvemos el mensaje a su orden original

def main():
    mensaje = input("Ingrese el mensaje a codificar: ")
    mensaje = list(mensaje)

    mensaje_codificado = hamming(mensaje)
    print("Mensaje codificado: ", ''.join(mensaje_codificado))

if __name__ == "__main__":
    main()
