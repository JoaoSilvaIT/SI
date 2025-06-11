import os

def calcular_ser(caminho_original: str, caminho_recebido: str) -> tuple:
    simbolos_errados = 0
    total_simbolos = 0
    try:
        total_simbolos = os.path.getsize(caminho_original)
        if total_simbolos == 0:
            return 0.0, 0, 0
        with open(caminho_original, 'rb') as f_orig, open(caminho_recebido, 'rb') as f_rec:
            while (byte_orig := f_orig.read(1)):
                byte_rec = f_rec.read(1)
                if not byte_rec:
                    break
                if byte_orig != byte_rec:
                    simbolos_errados += 1
        ser = simbolos_errados / total_simbolos
        return ser, simbolos_errados, total_simbolos
    except FileNotFoundError:
        print("Erro: Um dos ficheiros não foi encontrado.")
        return None, None, None
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None, None, None
    