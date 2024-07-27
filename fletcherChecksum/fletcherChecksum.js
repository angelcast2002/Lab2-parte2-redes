const net = require("node:net");
const mensajesValidos = [];
const mensajesInvalidos = [];

const verificarFletcher16 = (mensaje) => {
  let mensajeEnBytes = [];

  // Divide el mensaje en bytes
  for (let i = 0; i < mensaje.length - 16; i += 8) {
    mensajeEnBytes.push(parseInt(mensaje.substring(i, i + 8), 2));
  }

  // Separar el mensaje original y el checksum
  const mensajeOriginal = mensaje.substring(0, mensaje.length - 16);
  const checksum = parseInt(mensaje.substring(mensaje.length - 16), 2);

  let sum1 = 0;
  let sum2 = 0;

  // Calcular checksum usando Fletcher-16
  for (let i = 0; i < mensajeEnBytes.length; i++) {
    sum1 = (sum1 + mensajeEnBytes[i]) % 255;
    sum2 = (sum2 + sum1) % 255;
  }

  const checksumCalculado = (sum2 << 8) | sum1;

  // Comparar checksum calculado con el recibido
  return { esValido: checksum === checksumCalculado, mensajeOriginal };
};

const convertirBinarioAString = (mensaje) => {
  let mensajeEnString = "";

  for (let i = 0; i < mensaje.length; i += 8) {
    mensajeEnString += String.fromCharCode(
      parseInt(mensaje.substring(i, i + 8), 2)
    );
  }

  return mensajeEnString;
};

// Crear servidor TCP
const server = net.createServer((socket) => {
  console.log("Cliente conectado");

  // Evento al recibir datos del cliente
  socket.on("data", (data) => {
    const mensajeVerificado = verificarFletcher16(data.toString());
    if (mensajeVerificado.esValido) {
      console.log("El mensaje es válido");
      console.log(
        "Mensaje original:",
        convertirBinarioAString(mensajeVerificado.mensajeOriginal)
      );
      mensajesValidos.push(mensajeVerificado.mensajeOriginal);
    } else {
      console.log("El mensaje ha sido alterado");
      mensajesInvalidos.push(data.toString());
    }
  });

  // Evento cuando se cierra la conexión del cliente
  socket.on("close", () => {
    console.log("Cliente desconectado");
    // console.log("Mensajes válidos:", mensajesValidos);
    console.log("Cantidad de mensajes validos:", mensajesValidos.length);
    // console.log("Mensajes inválidos:", mensajesInvalidos);
    console.log("Cantidad de mensajes inválidos:", mensajesInvalidos.length);
  });

  // Manejar errores de conexión
  socket.on("error", (err) => {
    console.error("Error en conexión:", err);
  });
});

const puerto = 9000;
server.listen(puerto, () => {
  console.log(`Servidor TCP iniciado en puerto ${puerto}`);
});
