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

def binary_to_data(binary_str):
    byte_array = bytearray()
    for i in range(0, len(binary_str), 8):
        byte_array.append(int(binary_str[i:i+8], 2))
    return bytes(byte_array)

def main():
    input_msg = input("Ingrese el mensaje codificado en binario: \n")
    
    # Separar el mensaje y el CRC
    message, received_crc_bin = input_msg[:-32], input_msg[-32:]
    received_crc = int(received_crc_bin, 2)

    # mostrar el mensaje y sy crc32 por separado. 
    # Código de escape ANSI para el color verde
    GREEN = "\033[92m"
    RESET = "\033[0m"
    
    print(f"Mensaje: {message}\nCRC32: {GREEN}{received_crc_bin}{RESET}")
    
    calculated_crc = crc32_manual(message)
    
    if calculated_crc == received_crc:
        decoded_message = binary_to_data(message)
        try:
            decoded_message = decoded_message.decode('utf-8')
        except UnicodeDecodeError:
            pass
        print(f"No se detectaron errores. Mensaje original: \n{decoded_message}")
    else:
        print("Se detectaron errores.")
    
if __name__ == "__main__":
    main()
