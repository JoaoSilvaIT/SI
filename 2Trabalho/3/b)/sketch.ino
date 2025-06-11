const int N_FIBONACCI = 15; // Quantos números Fibonacci enviar

byte calcularCRC8(const char *data, int len) {
  byte crc = 0x00; // Valor inicial do CRC
  const byte polinomio = 0x0B; 

  for (int j = 0; j < len; j++) {
    crc ^= data[j]; // XOR com o próximo byte de dados
    for (int i = 0; i < 8; i++) { // Para cada bit do byte
      if ((crc & 0x80) != 0) { // Se o MSB do crc for 1
        crc = (byte)((crc << 1) ^ polinomio);
      } else {
        crc <<= 1;
      }
    }
  }
  return crc;
}

void setup() {
  Serial.begin(9600); // Inicia comunicação série a 9600 bps
  delay(2500); // Aumentado para 2.5 segundos para garantir

  long fib_n_2 = 0; // F(n-2), começa com F(0)
  long fib_n_1 = 1; // F(n-1), começa com F(1)
  long fib_atual;

  char buffer_numero_str[21]; // Buffer para converter número para string (long pode ter até 19-20 dígitos + sinal)
  byte crc_calculado;

  Serial.println("Iniciando transmissao Fibonacci com CRC-8:"); 

  if (N_FIBONACCI >= 1) {
    sprintf(buffer_numero_str, "%ld", fib_n_2); // Converte número para string
    crc_calculado = calcularCRC8(buffer_numero_str, strlen(buffer_numero_str));
    Serial.print(buffer_numero_str); // Envia o número
    Serial.print(",");               // Envia a vírgula separadora
    Serial.println(crc_calculado);   // Envia o CRC e a nova linha
  }

  if (N_FIBONACCI >= 2) {
    sprintf(buffer_numero_str, "%ld", fib_n_1);
    crc_calculado = calcularCRC8(buffer_numero_str, strlen(buffer_numero_str));
    Serial.print(buffer_numero_str);
    Serial.print(",");
    Serial.println(crc_calculado);
  }

  for (int i = 2; i < N_FIBONACCI; i++) {
    fib_atual = fib_n_1 + fib_n_2;
    sprintf(buffer_numero_str, "%ld", fib_atual);
    crc_calculado = calcularCRC8(buffer_numero_str, strlen(buffer_numero_str));
    
    Serial.print(buffer_numero_str); // Número
    Serial.print(",");               // Vírgula
    Serial.println(crc_calculado);   // CRC e nova linha
    
    fib_n_2 = fib_n_1;
    fib_n_1 = fib_atual;
    
    delay(150); // Pequeno delay entre envios para ajudar na sincronização com o PC
  }

  Serial.println("Fim da transmissao CRC."); 
}

void loop() {
}