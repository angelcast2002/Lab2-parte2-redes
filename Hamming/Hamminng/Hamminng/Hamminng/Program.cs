using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;

public class HammingDecoder
{
    public static string Decode(string message)
    {
        int[] msg = Array.ConvertAll(message.ToCharArray(), c => c - '0');
        Array.Reverse(msg);

        int r = 0;
        for (int i = 0; i < msg.Length; i++)
        {
            if ((i & (i + 1)) == 0)
            {
                r++;
            }
        }

        int errorPos = 0;
        for (int i = 0; i < r; i++)
        {
            int x = 1 << i;
            int parity = 0;
            for (int j = x - 1; j < msg.Length; j += 2 * x)
            {
                for (int k = j; k < j + x && k < msg.Length; k++)
                {
                    parity ^= msg[k];
                }
            }
            if (parity != 0)
            {
                errorPos += x;
            }
        }

        if (errorPos != 0)
        {
            if (errorPos - 1 < msg.Length)
            {
                Console.WriteLine("Error en la posición: " + errorPos);
                msg[errorPos - 1] ^= 1;
            }
        }
        else
        {
            Console.WriteLine("No hay errores");
        }

        List<int> data = new List<int>();
        for (int i = 0; i < msg.Length; i++)
        {
            if ((i & (i + 1)) != 0)
            {
                data.Add(msg[i]);
            }
        }

        data.Reverse();
        return string.Join("", data);
    }

    public static string BinarioATexto(string binario)
    {
        var stringBuilder = new StringBuilder();
        for (int i = 0; i < binario.Length; i += 8)
        {
            string byteString = binario.Substring(i, 8);
            byte byteValue = Convert.ToByte(byteString, 2);
            stringBuilder.Append((char)byteValue);
        }
        return stringBuilder.ToString();
    }

    public static void Main(string[] args)
    {
        TcpListener server = new TcpListener(IPAddress.Parse("127.0.0.1"), 65432);
        server.Start();
        Console.WriteLine("Esperando conexiones...");
        while (true)
        {
            using (TcpClient client = server.AcceptTcpClient())
            using (NetworkStream stream = client.GetStream())
            {
                byte[] buffer = new byte[1024];
                int bytesRead;
                while ((bytesRead = stream.Read(buffer, 0, buffer.Length)) != 0)
                {
                    Console.WriteLine("------------------------------------");
                    string receivedMessage = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    Console.WriteLine("Mensaje recibido: " + receivedMessage);

                    string decodedBits = Decode(receivedMessage);
                    string decodedMessage = BinarioATexto(decodedBits);
                    Console.WriteLine("Mensaje decodificado: " + decodedMessage);

                    // Enviamos la respuesta al cliente (indicar mensaje recibido)
                    byte[] response = Encoding.UTF8.GetBytes(decodedMessage);
                    stream.Write(response, 0, response.Length);


                }
            }
        }
    }
}
