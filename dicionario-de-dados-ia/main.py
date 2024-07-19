import cv2
import numpy as np
import pandas as pd

def process_image(image_path):
    """
    Processa a imagem para detectar a estrutura da tabela.

    Args:
    image_path (str): O caminho para a imagem da tabela.

    Returns:
    img: A imagem carregada.
    contours: Os contornos detectados na imagem.
    """
    # Carregar a imagem em tons de cinza
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Aplicar um threshold para binarizar a imagem
    _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    
    # Detectar linhas horizontais
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
    detect_horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    
    # Detectar linhas verticais
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
    detect_vertical = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    
    # Somar as linhas detectadas
    detected_lines = detect_horizontal + detect_vertical
    
    # Invertendo as cores novamente para encontrar contornos
    inverted_binary = cv2.bitwise_not(detected_lines)
    
    # Encontrar contornos
    contours, _ = cv2.findContours(inverted_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return img, contours

def extract_table_data(img, contours):
    """
    Extrai os dados das células da tabela.

    Args:
    img: A imagem carregada.
    contours: Os contornos detectados na imagem.

    Returns:
    list: Uma lista de listas contendo os dados de cada célula.
    """
    table_cells = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        table_cells.append((x, y, w, h))
    
    # Ordenar células primeiro por linha, depois por coluna
    table_cells = sorted(table_cells, key=lambda cell: (cell[1], cell[0]))
    
    return table_cells

def generate_table_description(data):
    """
    Gera uma descrição simples para a tabela.

    Args:
    data (list): Uma lista de listas contendo os dados de cada célula.

    Returns:
    str: A descrição gerada para a tabela.
    """
    description = "A tabela contém as seguintes colunas:\n"
    for i in range(len(data[0])):
        description += f"- Coluna {i + 1}: {len(data)} valores\n"
    return description

def document_table(image_path):
    """
    Documenta uma tabela a partir de uma imagem gerando descrições automáticas para cada coluna.

    Args:
    image_path (str): O caminho para a imagem da tabela.

    Returns:
    pd.DataFrame: Um DataFrame contendo as descrições das colunas e da tabela.
    """
    img, contours = process_image(image_path)
    table_cells = extract_table_data(img, contours)
    
    # Criar DataFrame da tabela
    data = []
    current_row = []
    prev_y = table_cells[0][1]
    
    for cell in table_cells:
        x, y, w, h = cell
        if y > prev_y + 10:
            data.append(current_row)
            current_row = []
            prev_y = y
        current_row.append(f"Cell at Coluna {x}, Linha {y}")
    data.append(current_row)
    
    # Gerar descrição da tabela
    table_description = generate_table_description(data)
    print(table_description)
    
    # Criar DataFrame
    max_cols = max(len(row) for row in data)
    df_data = []
    for row in data:
        if len(row) < max_cols:
            row.extend([''] * (max_cols - len(row)))
        df_data.append(row)
    
    df = pd.DataFrame(df_data, columns=[f"Coluna {i+1}" for i in range(max_cols)])
    
    return df, table_description

# Caminho para a imagem da tabela (substitua pelo caminho da sua imagem)
image_path = './img/tabela.png'

# Documenta a tabela
df, table_description = document_table(image_path)

# Salva as descrições das colunas em um novo arquivo CSV
df.to_csv('documentacao_da_tabela.csv', index=False)

print("Documentação da tabela criada com sucesso.")
