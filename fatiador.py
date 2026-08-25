import os

def fatiar_documento(nome_arquivo, limite_caracteres=90000):
    if not os.path.exists(nome_arquivo):
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado na pasta.")
        return

    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        numero_parte = 1
        pedaco_atual = []
        tamanho_atual = 0
        
        for linha in f:
            tamanho_linha = len(linha)
            
            # Se a linha atual fizer ultrapassar o limite, salva o arquivo e inicia o próximo
            if tamanho_atual + tamanho_linha > limite_caracteres and tamanho_atual > 0:
                nome_saida = f"doc_parte_{numero_parte}.txt"
                with open(nome_saida, 'w', encoding='utf-8') as out_f:
                    out_f.writelines(pedaco_atual)
                
                print(f"✅ {nome_saida} gerado com sucesso ({tamanho_atual} caracteres).")
                
                numero_parte += 1
                pedaco_atual = [linha]
                tamanho_atual = tamanho_linha
            else:
                pedaco_atual.append(linha)
                tamanho_atual += tamanho_linha
        
        # Salva o último arquivo com o que sobrou
        if pedaco_atual:
            nome_saida = f"doc_parte_{numero_parte}.txt"
            with open(nome_saida, 'w', encoding='utf-8') as out_f:
                out_f.writelines(pedaco_atual)
            print(f"✅ {nome_saida} gerado com sucesso ({tamanho_atual} caracteres).")

# Executando o script no seu arquivo mestre
arquivo_mestre = "flet_documentacao_mestre.txt"
print("Iniciando o fatiamento...")
fatiar_documento(arquivo_mestre)
print("Missão cumprida! Pode enviar as partes no chat.")