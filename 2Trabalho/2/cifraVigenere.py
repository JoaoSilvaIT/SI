def processar_vigenere(caminho_entrada, caminho_saida, chave, modo):
    try:
        chave_bytes = chave.encode('utf-8')
        i = 0
        with open(caminho_entrada, 'rb') as f_in, open(caminho_saida, 'wb') as f_out:
            while (byte := f_in.read(1)):
                byte_int = int.from_bytes(byte, 'big')
                chave_int = chave_bytes[i % len(chave_bytes)]
                if modo == 'cifrar':
                    byte_processado = (byte_int + chave_int) % 256
                elif modo == 'decifrar':
                    byte_processado = (byte_int - chave_int + 256) % 256
                else:
                    raise ValueError("Modo deve ser 'cifrar' ou 'decifrar'")
                f_out.write(byte_processado.to_bytes(1, 'big'))
                i += 1
    except FileNotFoundError:
        print(f"ERRO de Cifra: Ficheiro de entrada '{caminho_entrada}' não encontrado.")
        