import serial
import time
import random 
import traceback

def calcular_crc8_py(data_bytes: bytes) -> int:
    """Calcula CRC-8 para uma sequência de bytes. Polinómio 0x0B (X³ + X + 1)."""
    crc = 0x00
    polinomio = 0x0B  # X³ + X + 1 = 1011 (binário) = 0x0B (hexadecimal)

    for byte in data_bytes:
        crc ^= byte
        for _ in range(8):
            if (crc & 0x80) != 0:
                crc = (crc << 1) ^ polinomio
            else:
                crc <<= 1
            crc &= 0xFF 
    return crc

def introduzir_erro_bit_unico(data_bytes: bytes, posicao_bit: int = -1) -> bytearray:
    dados_corrompidos = bytearray(data_bytes) 
    total_bits = len(dados_corrompidos) * 8
    if total_bits == 0:
        return dados_corrompidos

    if posicao_bit == -1: 
        posicao_bit_erro = random.randint(0, total_bits - 1)
    else:
        posicao_bit_erro = posicao_bit % total_bits
        
    byte_idx = posicao_bit_erro // 8
    bit_idx_no_byte = posicao_bit_erro % 8

    dados_corrompidos[byte_idx] ^= (1 << bit_idx_no_byte) 
    
    print(f"    -> Erro de 1 bit introduzido no byte {byte_idx} (0-indexado), bit de ordem {bit_idx_no_byte} (0=LSB)")
    return dados_corrompidos

def introduzir_erro_rajada(data_bytes: bytes, inicio_bit: int = -1, comprimento_rajada: int = 3) -> bytearray:
    dados_corrompidos = bytearray(data_bytes)
    total_bits = len(dados_corrompidos) * 8
    if total_bits == 0 or comprimento_rajada <= 0:
        return dados_corrompidos
    comprimento_rajada = min(comprimento_rajada, total_bits)
    if inicio_bit == -1: 
        if total_bits < comprimento_rajada: 
            inicio_bit_erro = 0
        else:
            inicio_bit_erro = random.randint(0, total_bits - comprimento_rajada)
    else:
        inicio_bit_erro = inicio_bit % total_bits
        if inicio_bit_erro + comprimento_rajada > total_bits:
            comprimento_rajada = total_bits - inicio_bit_erro
    print(f"    -> Erro de rajada introduzido a partir do bit {inicio_bit_erro} (comprimento {comprimento_rajada})")
    for i in range(comprimento_rajada):
        pos_bit_atual = inicio_bit_erro + i
        if pos_bit_atual >= total_bits: 
            break
        byte_idx = pos_bit_atual // 8
        bit_idx_no_byte = pos_bit_atual % 8 
        dados_corrompidos[byte_idx] ^= (1 << bit_idx_no_byte)
    return dados_corrompidos

PORTA_SERIAL = "/dev/ttyUSB0"  
BAUD_RATE = 9600
TIMEOUT_LEITURA = 3 

if __name__ == "__main__":
    print(f"A tentar ligar a {PORTA_SERIAL} com baud rate {BAUD_RATE}...")
    try:
        with serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=TIMEOUT_LEITURA) as arduino_serial:
            print(f"Ligado a {PORTA_SERIAL}. A aguardar dados com CRC...")
            time.sleep(1.5) # Ajusta conforme o delay no setup do Arduino
            resultados_testes_crc = [] 
            while True:
                try:
                    linha_bytes_serial = arduino_serial.readline() 
                    if not linha_bytes_serial:
                        print("Timeout ou linha vazia ao ler da porta série. Fim da recepção presumido.")
                        break 
                    linha_str_recebida = linha_bytes_serial.decode('utf-8', errors='replace').strip()
                    print(f"\nRecebido (raw): '{linha_str_recebida}'")
                    if "Fim da transmissao CRC." in linha_str_recebida:
                        print("Mensagem de fim de transmissão CRC recebida do Arduino.")
                        break 
                    if "Iniciando transmissao Fibonacci com CRC-8:" in linha_str_recebida:
                        print("Cabeçalho de transmissão CRC recebido.")
                        continue # Pula para a próxima leitura
                    if not linha_str_recebida or "," not in linha_str_recebida:
                        print(f"  Aviso: Linha de DADOS mal formada ou vazia, ignorando: '{linha_str_recebida}'")
                        continue
                    try:
                        numero_str_original, crc_recebido_str = linha_str_recebida.split(',')
                        crc_recebido_int = int(crc_recebido_str)
                        dados_para_crc_bytes = numero_str_original.encode('utf-8') 
                    except ValueError:
                        print(f"  Erro ao parsear número ou CRC da linha de DADOS: '{linha_str_recebida}'")
                        continue
                    print(f"  Número (str): '{numero_str_original}', CRC Recebido do Arduino (int): {crc_recebido_int} (0x{crc_recebido_int:02X})")
                    print("  Teste 1: Verificação CRC nos dados originais (sem erro introduzido)")
                    crc_calculado_pc_sem_erro = calcular_crc8_py(dados_para_crc_bytes)
                    detecao_sem_erro = "NÃO DETETADO (CORRETO, dados íntegros)" if crc_calculado_pc_sem_erro == crc_recebido_int else "ERRO DETETADO (FALSO POSITIVO! VERIFICAR LÓGICA CRC!)"
                    print(f"    CRC Calculado pelo PC: {crc_calculado_pc_sem_erro} (0x{crc_calculado_pc_sem_erro:02X}), Resultado: {detecao_sem_erro}")
                    resultados_testes_crc.append({
                        'numero': numero_str_original, 'tipo_erro': 'Nenhum', 
                        'crc_arduino': crc_recebido_int, 'crc_pc_pos_erro': crc_calculado_pc_sem_erro,
                        'erro_detetado': crc_calculado_pc_sem_erro != crc_recebido_int
                    })

                    print("  Teste 2: Verificação CRC com erro de bit ÚNICO introduzido")
                    if len(dados_para_crc_bytes) > 0:
                        dados_corrompidos_bit_unico = introduzir_erro_bit_unico(dados_para_crc_bytes) 
                        crc_calculado_pc_bit_unico = calcular_crc8_py(bytes(dados_corrompidos_bit_unico)) 
                        erro_detetado_bit_unico = crc_calculado_pc_bit_unico != crc_recebido_int
                        print(f"    Dados corrompidos (bit único): {dados_corrompidos_bit_unico.decode('utf-8', errors='replace') if len(dados_corrompidos_bit_unico) < 30 else '...'}")
                        print(f"    CRC Calculado pelo PC (após erro): {crc_calculado_pc_bit_unico} (0x{crc_calculado_pc_bit_unico:02X}), Erro Detetado pelo CRC: {erro_detetado_bit_unico}")
                        resultados_testes_crc.append({
                            'numero': numero_str_original, 'tipo_erro': 'Bit Único', 
                            'crc_arduino': crc_recebido_int, 'crc_pc_pos_erro': crc_calculado_pc_bit_unico,
                            'erro_detetado': erro_detetado_bit_unico
                        })
                    else:
                        print("    Dados vazios, não é possível introduzir erro de bit único.")

                    print("  Teste 3: Verificação CRC com erro de RAJADA introduzido")
                    if len(dados_para_crc_bytes) > 0:
                        comprimento_rajada_teste = min(3, len(dados_para_crc_bytes) * 8) 
                        if comprimento_rajada_teste > 0:
                            dados_corrompidos_rajada = introduzir_erro_rajada(dados_para_crc_bytes, comprimento_rajada=comprimento_rajada_teste)
                            crc_calculado_pc_rajada = calcular_crc8_py(bytes(dados_corrompidos_rajada))
                            erro_detetado_rajada = crc_calculado_pc_rajada != crc_recebido_int
                            print(f"    Dados corrompidos (rajada): {dados_corrompidos_rajada.decode('utf-8', errors='replace') if len(dados_corrompidos_rajada) < 30 else '...'}")
                            print(f"    CRC Calculado pelo PC (após erro): {crc_calculado_pc_rajada} (0x{crc_calculado_pc_rajada:02X}), Erro Detetado pelo CRC: {erro_detetado_rajada}")
                            resultados_testes_crc.append({
                                'numero': numero_str_original, 'tipo_erro': f'Rajada ({comprimento_rajada_teste} bits)', 
                                'crc_arduino': crc_recebido_int, 'crc_pc_pos_erro': crc_calculado_pc_rajada,
                                'erro_detetado': erro_detetado_rajada
                            })
                        else:
                            print("    Comprimento de rajada zero, não é possível introduzir erro de rajada.")
                    else:
                        print("    Dados vazios, não é possível introduzir erro de rajada.")
                except serial.SerialException as e_loop:
                    print(f"Erro na porta série durante a leitura no loop: {e_loop}")
                    break 
                except KeyboardInterrupt:
                    print("\nLeitura interrompida pelo utilizador.")
                    break 
                except Exception as e_inner_loop:
                    print(f"Erro inesperado dentro do loop de leitura: {e_inner_loop}")
                    traceback.print_exc()
                    continue 
            print("\n\n--- RESUMO FINAL DOS TESTES CRC ---")
            if resultados_testes_crc:
                print(f"{'Número':<8} | {'Tipo Erro':<18} | {'CRC Arduino':<12} | {'CRC PC (c/ erro)':<18} | {'Erro Detetado':<15}")
                print("-" * 80)
                for res in resultados_testes_crc:
                    detetado_str = "SIM" if res['erro_detetado'] else "NÃO"
                    # Lógica para Falso Positivo/Negativo
                    if res['tipo_erro'] == 'Nenhum':
                        if res['erro_detetado']: # Se detetou erro quando não havia
                            detetado_str = "NÃO (FALSO POSITIVO!)"
                        else: # Se não detetou erro e não havia (correto)
                            detetado_str = "NÃO"
                    elif res['tipo_erro'] != 'Nenhum':
                        if not res['erro_detetado']: # Se não detetou erro quando havia
                            detetado_str = "NÃO (FALSO NEGATIVO!)"
                        # else: SIM (correto) já está coberto

                    print(f"{res['numero']:<8} | {res['tipo_erro']:<18} | 0x{res['crc_arduino']:02X}{'':<10} | 0x{res['crc_pc_pos_erro']:02X}{'':<16} | {detetado_str:<15}")
            else:
                print("Nenhum resultado de teste CRC para apresentar.")
    except serial.SerialException as e_main:
        print(f"ERRO CRÍTICO: Não foi possível abrir ou comunicar com a porta série {PORTA_SERIAL}: {e_main}")
        print("Verifica se a porta está correta, se o Arduino está ligado, se o baud rate coincide e se tens permissões.")
    except Exception as e_geral_main:
        print(f"Ocorreu um erro geral inesperado no script: {e_geral_main}")
        traceback.print_exc()