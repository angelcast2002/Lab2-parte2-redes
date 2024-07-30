package main

import (
	"fmt"
	"net"
	"strconv"
)

func crc32Manual(data string) uint32 {
	crc := uint32(0xFFFFFFFF)
	polynomial := uint32(0xEDB88320)

	for i := 0; i < len(data); i += 8 {
		byte, _ := strconv.ParseUint(data[i:i+8], 2, 32)
		crc ^= uint32(byte)
		for j := 0; j < 8; j++ {
			if crc&1 != 0 {
				crc = (crc >> 1) ^ polynomial
			} else {
				crc >>= 1
			}
		}
	}

	return crc ^ 0xFFFFFFFF
}

func main() {
	addr := net.UDPAddr{
		Port: 12345,
		IP:   net.ParseIP("127.0.0.1"),
	}

	conn, err := net.ListenUDP("udp", &addr)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer conn.Close()

	buffer := make([]byte, 1024)
	for {
		n, addr, err := conn.ReadFromUDP(buffer)
		if err != nil {
			fmt.Println(err)
			return
		}

		receivedMsg := string(buffer[:n])
		data := receivedMsg[:len(receivedMsg)-32]
		receivedCrcStr := receivedMsg[len(receivedMsg)-32:]
		receivedCrc, _ := strconv.ParseUint(receivedCrcStr, 2, 32)
		computedCrc := crc32Manual(data)

		response := "valid"
		if uint32(receivedCrc) != computedCrc {
			response = "invalid"
		}

		// Send response back to encoder
		conn.WriteToUDP([]byte(response), addr)

		fmt.Println("Mensaje recibido: ", data)
		if response == "valid" {
			fmt.Println("Mensaje sin errores")
		} else {
			fmt.Println("Errores detectados")
		}
	}
}
