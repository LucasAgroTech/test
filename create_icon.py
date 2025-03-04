from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """
    Cria um ícone simples para o aplicativo Pipeline EMBRAPII SRInfo.
    Requer a biblioteca Pillow (PIL).
    """
    try:
        # Tamanhos de ícone para Windows
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # Cores
        background_color = (0, 102, 204)  # Azul
        text_color = (255, 255, 255)  # Branco
        
        # Criar imagens para cada tamanho
        images = []
        for size in sizes:
            # Criar imagem com fundo azul
            img = Image.new('RGB', size, color=background_color)
            draw = ImageDraw.Draw(img)
            
            # Adicionar texto (iniciais)
            try:
                # Tentar usar uma fonte padrão
                font_size = max(8, int(size[0] / 3))
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Se não encontrar a fonte, usar a fonte padrão
                font = ImageFont.load_default()
            
            # Calcular posição do texto para centralizar
            text = "PE"
            try:
                text_width, text_height = draw.textsize(text, font=font)
            except:
                # Para versões mais recentes do Pillow
                text_width, text_height = font.getsize(text)
            
            position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
            
            # Desenhar texto
            draw.text(position, text, fill=text_color, font=font)
            
            # Adicionar à lista de imagens
            images.append(img)
        
        # Salvar como arquivo .ico
        icon_path = "pipeline_icon.ico"
        images[0].save(icon_path, format="ICO", sizes=[(s[0], s[1]) for s in sizes], append_images=images[1:])
        
        print(f"Ícone criado com sucesso: {os.path.abspath(icon_path)}")
        return os.path.abspath(icon_path)
    
    except Exception as e:
        print(f"Erro ao criar ícone: {str(e)}")
        return None

if __name__ == "__main__":
    create_icon()
