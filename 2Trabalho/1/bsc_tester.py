import os
from bsc import bsc
from calcular_ber import calcular_ber
from calcular_ser import calcular_ser

if __name__ == '__main__':
    ficheiro_original = "alice29.txt"
    ficheiro_recebido = "recebido.txt"
    probabilidade_erro = 0.1 
    print(f"A ler o ficheiro de entrada: '{ficheiro_original}'")
    bsc(ficheiro_original, ficheiro_recebido, probabilidade_erro)
    if os.path.exists(ficheiro_recebido):
        print(f"Canal BSC simulado com p = {probabilidade_erro}. Ficheiro recebido: '{ficheiro_recebido}'\n")
        ber, bits_errados, total_bits = calcular_ber(ficheiro_original, ficheiro_recebido)
        if ber is not None:
            print("--- Análise de Erro de Bit (BER) ---")
            print(f"Total de bits transmitidos: {total_bits}")
            print(f"Total de bits errados: {bits_errados}")
            print(f"BER (taxa de erro por bit): {ber:.6f} (ou {ber:.4%})")
        print("-" * 35)
        ser, simbolos_errados, total_simbolos = calcular_ser(ficheiro_original, ficheiro_recebido)
        if ser is not None:
            print("--- Análise de Erro de Símbolo (SER) ---")
            print(f"Total de símbolos (bytes) transmitidos: {total_simbolos}")
            print(f"Total de símbolos (bytes) errados: {simbolos_errados}")
            print(f"SER (taxa de erro por símbolo): {ser:.6f} (ou {ser:.4%})")