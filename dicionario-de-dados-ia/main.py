import json
import cv2

def generate_table_description(json_data):
    """
    Gera uma breve descrição da tabela com base nas colunas fornecidas.
    """
    table_name = json_data.get('nome_tabela', 'Tabela sem nome')
    column_names = json_data.get('nome_colunas', [])
    
    if not column_names:
        return f"A tabela '{table_name}' não possui colunas definidas."
    
    description = f"A tabela '{table_name}' contém as seguintes colunas: "
    description += ', '.join(column_names) + "."
    
    return description

def main(json_file_path, image_path):
    # Ler o arquivo JSON
    with open(json_file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    # Verificar se o campo 'comentario' está vazio
    if not json_data.get('comentario'):
        # Gerar uma breve descrição da tabela
        description = generate_table_description(json_data)
        print(description)
        
        # Carregar e exibir a imagem relacionada usando OpenCV
        image = cv2.imread(image_path)
        
        if image is not None:
            # Exibir a imagem
            cv2.imshow('Imagem Relacionada à Tabela', image)
            # Adicionar o texto de descrição na imagem
            cv2.putText(image, description, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('Imagem com Descrição', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print(f"Erro: Não foi possível carregar a imagem em {image_path}")
    else:
        print(f"Comentário existente: {json_data['comentario']}")

# Caminho para o arquivo JSON
json_file_path = './fontes-dados/tabela.json'  # Substitua pelo caminho do seu arquivo JSON
# Caminho para a imagem
image_path = './fontes-dados/tabela.png'  # Substitua pelo caminho da sua imagem

# Chamar a função principal
main(json_file_path, image_path)