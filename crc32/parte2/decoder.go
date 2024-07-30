package main

import (
	"fmt"
	"strconv"
)

func crc32(data string) uint32 {
	crc := uint32(0xFFFFFFFF)
	polynomial := uint32(0xEDB88320)

	for i := 0; i < len(data); i += 8 {
		byte, _ := strconv.ParseUint(data[i:i+8], 2, 8)
		crc ^= uint32(byte)
		for j := 0; j < 8; j++ {
			if crc&1 == 1 {
				crc = (crc >> 1) ^ polynomial
			} else {
				crc >>= 1
			}
		}
	}

	return crc ^ 0xFFFFFFFF
}

func binaryToData(binaryStr string) []byte {
	byteArray := make([]byte, len(binaryStr)/8)
	for i := 0; i < len(binaryStr); i += 8 {
		byteVal, _ := strconv.ParseUint(binaryStr[i:i+8], 2, 8)
		byteArray[i/8] = byte(byteVal)
	}
	return byteArray
}

func main() {
	var inputMsg string
	fmt.Println("Ingrese el mensaje codificado en binario: ")
	fmt.Scanln(&inputMsg)

	message := inputMsg[:len(inputMsg)-32]
	receivedCrcBin := inputMsg[len(inputMsg)-32:]
	receivedCrc, _ := strconv.ParseUint(receivedCrcBin, 2, 32)

	calculatedCrc := crc32(message)
	if calculatedCrc == uint32(receivedCrc) {
		decodedMessage := binaryToData(message)
		fmt.Println("No se detectaron errores. Mensaje original: ")
		fmt.Println(string(decodedMessage))
	} else {
		fmt.Println("Se detectaron errores.")
	}
}
