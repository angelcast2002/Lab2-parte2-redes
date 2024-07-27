package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

// Convierte una cadena a su representación binaria
func stringToBinary(s string) string {
	var result string
	for _, c := range s {
		result += fmt.Sprintf("%08b", c)
	}
	return result
}

// Convierte un entero a su representación binaria
func intToBinary(n int) string {
	return fmt.Sprintf("%064b", n)
}

// Función genérica para convertir diferentes tipos de datos a binario
func toBinary(data string) (string, error) {
	if n, err := strconv.Atoi(data); err == nil {
		return intToBinary(n), nil
	} else {
		return stringToBinary(data), nil
	}
}

// Cálculo manual del CRC32
func crc32(data []byte) uint32 {
	crc := ^uint32(0)
	for _, b := range data {
		crc ^= uint32(b)
		for i := 0; i < 8; i++ {
			if crc&1 == 1 {
				crc = (crc >> 1) ^ 0xEDB88320
			} else {
				crc >>= 1
			}
		}
	}
	return ^crc
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Ingrese el mensaje: ")
	input, _ := reader.ReadString('\n')
	input = strings.TrimSpace(input)

	binaryData, err := toBinary(input)
	if err != nil {
		log.Fatalf("Error converting to binary: %v", err)
	}

	// Cálculo del CRC32
	crc := crc32([]byte(input))
	crcBinary := fmt.Sprintf("%032b", crc)

	encodedMessage := binaryData + crcBinary

	fmt.Println("Encoded message:", encodedMessage)
}
