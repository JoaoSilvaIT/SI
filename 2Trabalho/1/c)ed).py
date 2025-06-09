import os
import random
from bsc import bsc  
from calcular_ber import calcular_ber  
from calcular_ser import calcular_ser  

# --- Funções Helper para manipulação de bits ---
def read_bits(file_path):
    with open(file_path, 'rb') as f:
        while (byte := f.read(1)):
            for i in range(8): yield (int.from_bytes(byte, 'big') >> (7 - i)) & 1

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

# --- Códigos de Canal Corrigidos ---
def codificador_repeticao_3_1(c_e, c_s):
    def gen_coded_bits():
        for bit in read_bits(c_e):
            yield from [bit, bit, bit]
    write_bits(c_s, gen_coded_bits())

def descodificador_repeticao_3_1(c_e, c_s, c_o):
    def gen_decoded_bits():
        bit_source = read_bits(c_e)
        while True:
            try:
                # Tenta ler 3 bits de uma vez
                bloco = [next(bit_source) for _ in range(3)]
                yield 1 if sum(bloco) >= 2 else 0
            except StopIteration:
                # Se não houver mais bits, o loop termina naturalmente
                break
    tamanho_original_bits = os.path.getsize(c_o) * 8
    write_bits(c_s, gen_decoded_bits(), tamanho_original_bits)

def codificador_hamming_7_4(c_e, c_s):
    def gen_coded_bits():
        bit_source = read_bits(c_e)
        while True:
            m = [next(bit_source, None) for _ in range(4)]
            if m[0] is None: break
            m = [(b if b is not None else 0) for b in m]
            m0,m1,m2,m3=m; b0=m1^m2^m3; b1=m0^m1^m3; b2=m0^m2^m3
            yield from [m0,m1,m2,m3,b0,b1,b2]
    write_bits(c_s, gen_coded_bits())

def descodificador_hamming_7_4(c_e, c_s, c_o):
    mapa = {1:6, 2:5, 3:0, 4:4, 5:2, 6:1, 7:3}
    def gen_decoded_bits():
        bit_source = read_bits(c_e)
        while True:
            try:
                y = [next(bit_source) for _ in range(7)]
                y0,y1,y2,y3,y4,y5,y6=y; s0=y1^y2^y3^y4; s1=y0^y1^y3^y5; s2=y0^y2^y3^y6
                s = s2*4+s1*2+s0
                if s in mapa: y[mapa[s]]^=1
                yield from y[:4]
            except StopIteration:
                break
    tamanho_original_bits = os.path.getsize(c_o) * 8
    write_bits(c_s, gen_decoded_bits(), tamanho_original_bits)

# --- SCRIPT PRINCIPAL DE SIMULAÇÃO ---
if __name__ == "__main__":
    ficheiro_original = "alice29.txt"
    probabilidade_a_testar = 0.01

    if not os.path.exists(ficheiro_original):
        print(f"ERRO: Ficheiro '{ficheiro_original}' não encontrado.")
    else:
        p = probabilidade_a_testar
        print(f"\n" + "="*55)
        print(f"SIMULAÇÃO COM PROBABILIDADE DE ERRO p = {p:.3f} ({p:.1%})")
        print("="*55)

        print("(i)   Cenário: Sem Código de Controlo")
        saida_bsc = "recebido_sem_codigo.bin"
        if bsc(ficheiro_original, saida_bsc, p):
            ber_val, _, _ = calcular_ber(ficheiro_original, saida_bsc)
            ser_val, _, _ = calcular_ser(ficheiro_original, saida_bsc)
            if ber_val is not None:
                print(f"      BER Final = {ber_val:.6f} ({ber_val:.4%}) | SER Final = {ser_val:.6f} ({ser_val:.4%})\n")

        print("(ii)  Cenário: Código de Repetição (3,1)")
        f_cod="cod_rep.bin"; f_rec="rec_rep.bin"; f_dec="dec_rep.txt"
        codificador_repeticao_3_1(ficheiro_original, f_cod)
        if bsc(f_cod, f_rec, p):
            descodificador_repeticao_3_1(f_rec, f_dec, ficheiro_original)
            ber_val, _, _ = calcular_ber(ficheiro_original, f_dec)
            ser_val, _, _ = calcular_ser(ficheiro_original, f_dec)
            if ber_val is not None:
                print(f"      BER Final = {ber_val:.6f} ({ber_val:.4%}) | SER Final = {ser_val:.6f} ({ser_val:.4%})\n")

        print("(iii) Cenário: Código de Hamming (7,4)")
        f_cod="cod_ham.bin"; f_rec="rec_ham.bin"; f_dec="dec_ham.txt"
        codificador_hamming_7_4(ficheiro_original, f_cod)
        if bsc(f_cod, f_rec, p):
            descodificador_hamming_7_4(f_rec, f_dec, ficheiro_original)
            ber_val, _, _ = calcular_ber(ficheiro_original, f_dec)
            ser_val, _, _ = calcular_ser(ficheiro_original, f_dec)
            if ber_val is not None:
                print(f"      BER Final = {ber_val:.6f} ({ber_val:.4%}) | SER Final = {ser_val:.6f} ({ser_val:.4%})")
                