import os
import random
from bsc import bsc
from calcular_ber import calcular_ber
from calcular_ser import calcular_ser

# Funcao para ler bits de um ficheiro
def read_bits(file_path):
    with open(file_path, 'rb') as f:
        while (byte := f.read(1)):
            for i in range(8):
                yield (int.from_bytes(byte, 'big') >> (7 - i)) & 1

# Funcao para escrever bits num ficheiro
def write_bits(file_path, bit_stream, total_bits_a_escrever=None):
    buffer, count = 0, 0
    bits_escritos = 0
    with open(file_path, 'wb') as f:
        for bit in bit_stream:
            if total_bits_a_escrever is not None and bits_escritos >= total_bits_a_escrever:
                break
            buffer = (buffer << 1) | bit
            count += 1
            bits_escritos += 1
            if count == 8:
                f.write(buffer.to_bytes(1, 'big'))
                buffer, count = 0, 0
        if count > 0 and (total_bits_a_escrever is None or bits_escritos < total_bits_a_escrever):
            f.write((buffer << (8 - count)).to_bytes(1, 'big'))

# Codificador de Repeticao (3,1)
def codificador_repeticao_3_1(c_e, c_s):
    def gen_coded_bits():
        for bit in read_bits(c_e):
            yield from [bit, bit, bit]
    write_bits(c_s, gen_coded_bits())

# Descodificador de Repeticao (3,1)
def descodificador_repeticao_3_1(c_e, c_s, ficheiro_original):
    tamanho_original_bits = os.path.getsize(ficheiro_original) * 8
    def gen_decoded_bits():
        bits = iter(read_bits(c_e))
        try:
            while True:
                b1, b2, b3 = next(bits), next(bits), next(bits)
                yield 1 if (b1 + b2 + b3) > 1 else 0
        except StopIteration:
            pass
    write_bits(c_s, gen_decoded_bits(), tamanho_original_bits)

# Codificador de Hamming (7,4)
def codificador_hamming_7_4(c_e, c_s):
    def gen_coded_bits():
        bits = iter(read_bits(c_e))
        try:
            while True:
                d = [next(bits) for _ in range(4)]
                p1 = d[0] ^ d[1] ^ d[3]
                p2 = d[0] ^ d[2] ^ d[3]
                p3 = d[1] ^ d[2] ^ d[3]
                yield from [p1, p2, d[0], p3, d[1], d[2], d[3]]
        except StopIteration:
            pass
    write_bits(c_s, gen_coded_bits())

# Descodificador de Hamming (7,4)
def descodificador_hamming_7_4(c_e, c_s, ficheiro_original):
    tamanho_original_bits = os.path.getsize(ficheiro_original) * 8
    def gen_decoded_bits():
        bits = iter(read_bits(c_e))
        try:
            while True:
                r = [next(bits) for _ in range(7)]
                s1 = r[0] ^ r[2] ^ r[4] ^ r[6]
                s2 = r[1] ^ r[2] ^ r[5] ^ r[6]
                s3 = r[3] ^ r[4] ^ r[5] ^ r[6]
                sindrome = (s3 << 2) | (s2 << 1) | s1
                if sindrome > 0:
                    r[sindrome - 1] ^= 1 # Corrigir o bit em erro
                yield from [r[2], r[4], r[5], r[6]] # Retornar os bits de dados
        except StopIteration:
            pass
    write_bits(c_s, gen_decoded_bits(), tamanho_original_bits)


def main():
    ficheiro_original = "alice29.txt"
    # Lista com os 4 valores de probabilidade de erro (p) para testar
    probabilidades_erro = [0.001, 0.01, 0.05, 0.1]

    # Ciclo para executar a simulação para cada valor de p
    for p in probabilidades_erro:
        print(f"======================================================")
        print(f"      INICIANDO SIMULAÇÃO PARA p = {p}      ")
        print(f"======================================================\n")

        print("(i)   Cenário: Sem Código de Controlo de Erros")
        saida_bsc = "recebido_sem_codigo.bin"
        if bsc(ficheiro_original, saida_bsc, p):
            ber_val, _, _ = calcular_ber(ficheiro_original, saida_bsc)
            ser_val, _, _ = calcular_ser(ficheiro_original, saida_bsc)
            if ber_val is not None:
                print(f"      BER Final = {ber_val:.6f} ({ber_val:.4%}) | SER Final = {ser_val:.6f} ({ser_val:.4%})\n")

        print("(ii)  Cenário: Código de Repetição (3,1)")
        f_cod = "cod_rep.bin"
        f_rec = "rec_rep.bin"
        f_dec = "dec_rep.txt"
        codificador_repeticao_3_1(ficheiro_original, f_cod)
        if bsc(f_cod, f_rec, p):
            descodificador_repeticao_3_1(f_rec, f_dec, ficheiro_original)
            ber_val, _, _ = calcular_ber(ficheiro_original, f_dec)
            ser_val, _, _ = calcular_ser(ficheiro_original, f_dec)
            if ber_val is not None:
                print(f"      BER Final = {ber_val:.6f} ({ber_val:.4%}) | SER Final = {ser_val:.6f} ({ser_val:.4%})\n")

        print("(iii) Cenário: Código de Hamming (7,4)")
        f_cod = "cod_ham.bin"
        f_rec = "rec_ham.bin"
        f_dec = "dec_ham.txt"
        codificador_hamming_7_4(ficheiro_original, f_cod)
        if bsc(f_cod, f_rec, p):
            descodificador_hamming_7_4(f_rec, f_dec, ficheiro_original)
            ber_val, _, _ = calcular_ber(ficheiro_original, f_dec)
            ser_val, _, _ = calcular_ser(ficheiro_original, f_dec)
            if ber_val is not None:
                print(f"      BER Final = {ber_val:.6f} ({ber_val:.4%}) | SER Final = {ser_val:.6f} ({ser_val:.4%})\n")

if __name__ == "__main__":
    main()