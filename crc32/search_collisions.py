import random
import string

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

def string_to_binary(s):
    return ''.join(format(ord(c), '08b') for c in s)

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def main():
    length = 5  # Longitud de las cadenas aleatorias
    num_trials = 10000000000000  # Número de pruebas a realizar
    
    hashes = {}
    
    for _ in range(num_trials):
        random_str = generate_random_string(length)
        binary_str = string_to_binary(random_str)
        crc = crc32_manual(binary_str)
        
        if crc in hashes and hashes[crc] != random_str:
            print(f"Colisión encontrada: '{random_str}' y '{hashes[crc]}' tienen el mismo CRC32: {crc:08X}")
            break
        else:
            hashes[crc] = random_str
    else:
        print(f"No se encontraron colisiones en {num_trials} pruebas")

if __name__ == "__main__":
    main()
