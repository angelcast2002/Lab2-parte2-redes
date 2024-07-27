using System;
using System.Collections.Generic;

public class HammingDecoder
{
    public static string Decode(string message)
    {
        // Convertir mensaje a un arreglo de ints
        int[] msg = Array.ConvertAll(message.ToCharArray(), c => c - '0');

        // Invertir el orden de los bits
        Array.Reverse(msg);

        // Calcular la cantidad de bits de paridad
        int r = (int)Math.Ceiling(Math.Log2(msg.Length + 1));

        // Verificar si hay errores
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

        // Corregir errores si es necesario
        if (errorPos != 0)
        {
            Console.WriteLine("Error en la posición: " + errorPos);
            msg[errorPos - 1] ^= 1;
        }
        else
        {
            Console.WriteLine("No hay errores");
        }

        // Eliminar los bits de paridad
        List<int> data = new List<int>();
        for (int i = 0; i < msg.Length; i++)
        {
            if ((i & (i + 1)) != 0)
            {
                data.Add(msg[i]);
            }
        }

        // Reinvertir el orden de los bits y convertir a string
        data.Reverse();
        return string.Join("", data);
    }

    static void Main(string[] args)
    {
        Console.WriteLine("Ingrese el mensaje a decodificar: ");
        string message = Console.ReadLine();
        Console.WriteLine("Mensaje decodificado: " + Decode(message));
    }
}
