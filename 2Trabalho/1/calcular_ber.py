import os

def calcular_ber(caminho_original: str, caminho_recebido: str) -> tuple:
    bits_errados = 0
    total_bits = 0
    try:
        tamanho_original = os.path.getsize(caminho_original)
        total_bits = tamanho_original * 8
        if total_bits == 0:
            return 0.0, 0, 0
        with open(caminho_original, 'rb') as f_orig, open(caminho_recebido, 'rb') as f_rec:
            while (byte_orig := f_orig.read(1)):
                byte_rec = f_rec.read(1)
                if not byte_rec: # Se o ficheiro recebido for mais curto
                    break
                # XOR entre os bytes para encontrar os bits diferentes
                xor_result = int.from_bytes(byte_orig, 'big') ^ int.from_bytes(byte_rec, 'big')
                bits_errados += xor_result.bit_count()
        ber = bits_errados / total_bits
        return ber, bits_errados, total_bits
    except FileNotFoundError:
        print("Erro: Um dos ficheiros não foi encontrado.")
        return None, None, None
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None, None, None