"""
Script para salvar a imagem do logo da FURIA.
Coloque o arquivo de imagem 'furia-logo.png' no mesmo diretório que este script.
"""

import os
import shutil

def save_furia_logo():
    # Verifica se o arquivo do logo existe no diretório atual
    source_path = 'furia-logo.png'
    if not os.path.exists(source_path):
        print("Erro: O arquivo 'furia-logo.png' não foi encontrado.")
        print("Por favor, coloque o arquivo no mesmo diretório que este script.")
        return False
    
    # Cria diretório de destino se não existir
    dest_dir = os.path.join('static', 'images')
    os.makedirs(dest_dir, exist_ok=True)
    
    # Define o caminho de destino
    dest_path = os.path.join(dest_dir, 'furia-logo.png')
    
    # Copia o arquivo
    shutil.copyfile(source_path, dest_path)
    print(f"Logo da FURIA copiado com sucesso para {dest_path}")
    return True

if __name__ == "__main__":
    save_furia_logo()