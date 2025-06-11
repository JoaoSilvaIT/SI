const int N_FIBONACCI = 15;

void setup() {
  Serial.begin(9600); 
  delay(100);        
  long fib_n_2 = 0; // F(0)
  long fib_n_1 = 1; // F(1)
  long fib_atual;
  Serial.println("Iniciando transmissao da sequencia de Fibonacci:");
  if (N_FIBONACCI >= 1) {
    Serial.println(fib_n_2);
  }
  if (N_FIBONACCI >= 2) {
    Serial.println(fib_n_1);
  }
  for (int i = 2; i < N_FIBONACCI; i++) {
    fib_atual = fib_n_1 + fib_n_2;
    Serial.println(fib_atual); 
    fib_n_2 = fib_n_1;
    fib_n_1 = fib_atual;
    delay(100);
  }
  Serial.println("Fim da transmissao."); 
}
void loop() {
}