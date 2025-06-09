import os
import collections
import math

def analisar_ficheiro(caminho_ficheiro):
    """
    Analisa um ficheiro, calcula o seu tamanho e entropia.
    (Função baseada no seu ficheiro 'analiseFontes.py')
    """
    try:
        tamanho = os.path.getsize(caminho_ficheiro)
        if tamanho == 0:
            return {'tamanho': 0, 'entropia': 0}
        with open(caminho_ficheiro, 'rb') as f:
            dados = f.read()
        contagem = collections.Counter(dados)
        entropia = -sum((c / tamanho) * math.log2(c / tamanho) for c in contagem.values())
        return {'tamanho': tamanho, 'entropia': entropia}
    except FileNotFoundError:
        print(f"ERRO de Análise: Ficheiro não encontrado em '{caminho_ficheiro}'")
        return None