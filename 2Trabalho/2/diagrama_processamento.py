import os
import random
import shutil
from analiseFontes import analisar_ficheiro 
from cifraVigenere import processar_vigenere 

def codificador_fonte(caminho_entrada, caminho_saida):
    "TODO"
    shutil.copy(caminho_entrada, caminho_saida)

def descodificador_fonte(caminho_entrada, caminho_saida):
    "TODO"
    shutil.copy(caminho_entrada, caminho_saida)

def read_bits(file_path):
    with open(file_path, 'rb') as f:
        while (byte := f.read(1)):
            for i in range(8): yield (int.from_bytes(byte, 'big') >> (7 - i)) & 1

def write_bits(file_path, bit_stream, total_bits_a_escrever=None):
    buffer, count, bits_escritos = 0, 0, 0
    with open(file_path, 'wb') as f:
        for bit in bit_stream:
            if total_bits_a_escrever is not None and bits_escritos >= total_bits_a_escrever: break
            buffer = (buffer << 1) | bit; count += 1; bits_escritos += 1
            if count == 8: f.write(buffer.to_bytes(1, 'big')); buffer, count = 0, 0
        if count > 0 and (total_bits_a_escrever is None or bits_escritos < total_bits_a_escrever):
            f.write((buffer << (8 - count)).to_bytes(1, 'big'))

def codificador_canal_repeticao(c_e, c_s):
    def gen():
        for bit in read_bits(c_e): yield from [bit, bit, bit]
    write_bits(c_s, gen())

def descodificador_canal_repeticao(c_e, c_s, tamanho_original_bytes):
    def gen():
        bit_source = read_bits(c_e)
        while True:
            try:
                bloco = [next(bit_source) for _ in range(3)]
                yield 1 if sum(bloco) >= 2 else 0
            except StopIteration: break
    write_bits(c_s, gen(), tamanho_original_bytes * 8)

def simular_canal_bsc(c_e, c_s, p):
    with open(c_e, 'rb') as f_in, open(c_s, 'wb') as f_out:
        while (byte := f_in.read(1)):
            byte_int = int.from_bytes(byte, 'big'); byte_mod = 0
            for i in range(8):
                bit = (byte_int >> i) & 1
                if random.random() < p: bit ^= 1
                if bit: byte_mod |= (1 << i)
            f_out.write(byte_mod.to_bytes(1, 'big'))

if __name__ == "__main__":
    FICHEIRO_ENTRADA_A = "alice29.txt"
    CHAVE_VIGENERE = "SEGURANCA"
    PROBABILIDADE_BSC = 0.01
    PASTA_SAIDA = "artefactos_exercicio2"

    if not os.path.exists(FICHEIRO_ENTRADA_A):
        print(f"ERRO: O ficheiro de entrada '{FICHEIRO_ENTRADA_A}' não foi encontrado."); exit()
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    path_b = os.path.join(PASTA_SAIDA, "B_codificado_fonte.txt")
    path_c = os.path.join(PASTA_SAIDA, "C_cifrado.bin")
    path_c_codificado = os.path.join(PASTA_SAIDA, "C_codificado_canal.bin")
    path_d = os.path.join(PASTA_SAIDA, "D_transmitido_com_erros.bin")
    path_e_temp = os.path.join(PASTA_SAIDA, "E_descodificado_canal.bin")
    path_a_recuperado = os.path.join(PASTA_SAIDA, "A_recuperado.txt")

    print("\n" + "="*60); print("INICIANDO PROCESSO DE COMUNICAÇÃO DIGITAL"); print("="*60)

    # Etapa A: Ficheiro Original
    print("\n[ ETAPA A: Ficheiro Original ]")
    info_a = analisar_ficheiro(FICHEIRO_ENTRADA_A)
    print(f"  -> Ficheiro: '{FICHEIRO_ENTRADA_A}' | Tamanho: {info_a['tamanho']} bytes | Entropia: {info_a['entropia']:.4f} bits/símbolo")

    # Etapa B: Codificação de Fonte (A -> B)
    print("\n[ ETAPA B: Codificação de Fonte ]")
    codificador_fonte(FICHEIRO_ENTRADA_A, path_b)
    info_b = analisar_ficheiro(path_b)
    if info_a['tamanho'] > 0:
        taxa_compressao = (1 - info_b['tamanho'] / info_a['tamanho']) * 100
        print(f"  -> Ficheiro: '{path_b}' | Tamanho: {info_b['tamanho']} bytes | Compressão: {taxa_compressao:.2f}% (simulada)")

    # Etapa C: Cifra (B -> C)
    print("\n[ ETAPA C: Cifra ]")
    processar_vigenere(path_b, path_c, CHAVE_VIGENERE, modo='cifrar')
    info_c = analisar_ficheiro(path_c)
    print(f"  -> Ficheiro: '{path_c}' | Tamanho: {info_c['tamanho']} bytes | Entropia: {info_c['entropia']:.4f} bits/símbolo")

    # Etapa D: Codificação de Canal + Transmissão BSC (C -> D)
    print("\n[ ETAPA D: Codificação de Canal e Transmissão por BSC ]")
    codificador_canal_repeticao(path_c, path_c_codificado)
    info_c_codificado = analisar_ficheiro(path_c_codificado)
    print(f"  -> Tamanho após codificação de canal: {info_c_codificado['tamanho']} bytes (Redundância 3:1)")
    simular_canal_bsc(path_c_codificado, path_d, PROBABILIDADE_BSC)
    print(f"  -> Ficheiro transmitido com erros: '{path_d}'")

    # Etapa E: Descodificação de Canal, Decifra e Descodificação de Fonte (D -> A')
    print("\n[ ETAPA E: Receção, Descodificação, Decifra e Descodificação de Fonte ]")
    descodificador_canal_repeticao(path_d, path_e_temp, info_c['tamanho'])
    path_decifrado = os.path.join(PASTA_SAIDA, "E_decifrado.txt")
    processar_vigenere(path_e_temp, path_decifrado, CHAVE_VIGENERE, modo='decifrar')
    descodificador_fonte(path_decifrado, path_a_recuperado)
    info_a_recuperado = analisar_ficheiro(path_a_recuperado)
    print(f"  -> Ficheiro final recuperado: '{path_a_recuperado}' | Tamanho: {info_a_recuperado['tamanho']} bytes")

    # --- Verificação Final ---
    print("\n" + "="*60); print("VERIFICAÇÃO FINAL"); print("="*60)
    with open(FICHEIRO_ENTRADA_A, 'rb') as f1, open(path_a_recuperado, 'rb') as f2:
        if f1.read() == f2.read():
            print("✅ SUCESSO! O ficheiro recuperado é idêntico ao original.")
        else:
            print("❌ FALHA! O ficheiro recuperado é diferente do original devido a erros não corrigidos pelo Código de Canal.")