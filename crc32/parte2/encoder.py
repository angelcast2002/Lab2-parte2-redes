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

def main():
    input_msg = input("Ingrese el mensaje a codificar: \n")
    binary_str = data_to_binary(input_msg.encode())
    crc = crc32_manual(binary_str)
    crc_binary = format(crc, '032b')
    encoded_msg = binary_str + crc_binary
    print(f"Mensaje codificado en binario: \n{encoded_msg}")

if __name__ == "__main__":
    main()
