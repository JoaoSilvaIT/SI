import serial
import time

PORTA_SERIAL = "/dev/ttyUSB0" 
BAUD_RATE = 9600
TIMEOUT_LEITURA = 2

if __name__ == "__main__":
    try:
        with serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=TIMEOUT_LEITURA) as arduino_serial:
            print(f"Ligado a {PORTA_SERIAL}. A aguardar dados...")
            time.sleep(2)
            numeros_fibonacci_recebidos = []
            while True:
                try:
                    linha_bytes = arduino_serial.readline() 
                    if not linha_bytes:
                        print("Nenhum dado recebido (timeout) ou fim da linha vazia.")
                        break 
                    linha_str = linha_bytes.decode('utf-8', errors='replace').strip()
                    print(f"Recebido (raw): '{linha_str}'")
                    if "Fim da transmissao." in linha_str:
                        print("Mensagem de fim de transmissão recebida.")
                        break
                    if "Iniciando transmissao" in linha_str:
                        print("Cabeçalho de transmissão recebido.")
                        continue
                    if linha_str: 
                        try:
                            numero = int(linha_str)
                            numeros_fibonacci_recebidos.append(numero)
                            print(f"Numero convertido: {numero}")
                        except ValueError:
                            print(f"  Aviso: Não foi possível converter '{linha_str}' para inteiro.")
                except serial.SerialException as e:
                    print(f"Erro na porta série durante a leitura: {e}")
                    break
                except KeyboardInterrupt:
                    print("\nLeitura interrompida pelo utilizador.")
                    break
            print("\n--- Sequência de Fibonacci Recebida ---")
            if numeros_fibonacci_recebidos:
                for i, num in enumerate(numeros_fibonacci_recebidos):
                    print(f"F({i}) = {num}")
            else:
                print("Nenhum número de Fibonacci foi recebido/processado.")
    except serial.SerialException as e:
        print(f"Erro ao tentar abrir a porta série {PORTA_SERIAL}: {e}")
        print("Verifica se a porta está correta, se o Arduino está ligado e se o baud rate coincide.")
    except Exception as e_geral:
        print(f"Ocorreu um erro inesperado: {e_geral}")