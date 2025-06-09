import random

def bsc(caminho_entrada: str, caminho_saida: str, p: float):
    if not 0.0 <= p <= 1.0: raise ValueError("Probabilidade inválida")
    try:
        with open(caminho_entrada, 'rb') as f_in, open(caminho_saida, 'wb') as f_out:
            while (byte_lido := f_in.read(1)):
                byte_int = int.from_bytes(byte_lido, 'big')
                byte_mod_int = 0
                for i in range(8):
                    bit = (byte_int >> i) & 1
                    if random.random() < p: bit ^= 1
                    if bit == 1: byte_mod_int |= (1 << i)
                f_out.write(byte_mod_int.to_bytes(1, 'big'))
    except FileNotFoundError:
        print(f"ERRO: Ficheiro de entrada '{caminho_entrada}' não encontrado.")
        return False
    return True