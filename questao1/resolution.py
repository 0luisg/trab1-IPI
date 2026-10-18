import cv2
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. DEFINIÇÃO DAS FUNÇÕES
# ==========================================

def aumentar_por_2(img):
    # Função auxiliar para repetir os píxeis
    return np.repeat(np.repeat(img, 2, axis=0), 2, axis=1)

def TAM2(img, fator):
    # Aumenta a imagem iterativamente copiando o vizinho mais próximo
    n_iteracoes = int(np.log2(fator))
    resultado = img.copy()
    for _ in range(n_iteracoes):
        resultado = aumentar_por_2(resultado)
    return resultado

def TAMM(img):
    # Aumenta a imagem utilizando a média dos vizinhos
    img_f = img.astype(np.float32)
    h, w, c = img_f.shape
    res = np.zeros((h * 2, w * 2, c), dtype=np.float32)

    res[0::2, 0::2] = img_f
    res[0::2, 1:-1:2] = (img_f[:, :-1] + img_f[:, 1:]) / 2.0
    res[0::2, -1] = img_f[:, -1] 
    res[1:-1:2, :] = (res[0:-2:2, :] + res[2::2, :]) / 2.0
    res[-1, :] = res[-2, :] 

    return np.clip(res, 0, 255).astype(np.uint8)

def SUPERRES(img1, img2):
    # Combina duas imagens e preenche os buracos com média
    h, w, c = img1.shape
    res = np.zeros((h * 2, w * 2, c), dtype=np.float32)

    # Imagem 1 nas linhas e colunas pares (índices 0, 2, 4...)
    res[0::2, 0::2] = img1.astype(np.float32)
    # Imagem 2 nas linhas e colunas ímpares (índices 1, 3, 5...)
    res[1::2, 1::2] = img2.astype(np.float32)

    # CORREÇÃO DA IMAGEM 1 (buracos nas colunas ímpares das linhas pares)
    res[0::2, 1:-1:2] = (res[0::2, 0:-2:2] + res[0::2, 2::2]) / 2.0
    res[0::2, -1] = res[0::2, -2] 

    # CORREÇÃO DA IMAGEM 2 (buracos nas colunas pares das linhas ímpares)
    res[1::2, 0] = res[1::2, 1] # Primeira coluna copia a segunda
    res[1::2, 2::2] = (res[1::2, 1:-2:2] + res[1::2, 3::2]) / 2.0 # Média
    
    return np.clip(res, 0, 255).astype(np.uint8)

# ==========================================
# 2. TESTES E SALVAMENTO DAS IMAGENS
# ==========================================

# Carregar imagens originais
img_fruit1 = cv2.imread('FRUIT1.jpg')
img_fruit2 = cv2.imread('FRUIT2.jpg')

if img_fruit1 is not None and img_fruit2 is not None:
    # Converter de BGR (padrão do OpenCV) para RGB (para processamento e visualização corretos)
    img_fruit1 = cv2.cvtColor(img_fruit1, cv2.COLOR_BGR2RGB)
    img_fruit2 = cv2.cvtColor(img_fruit2, cv2.COLOR_BGR2RGB)


    # Redimensionar a imagem 2 para ter o mesmo tamanho da imagem 1
    # altura, largura = img_fruit1.shape[:2]
    # img_fruit2 = cv2.resize(img_fruit2, (largura, altura))

    # Executar as funções de processamento
    img_tam2_2 = TAM2(img_fruit1, 2)
    img_tam2_8 = TAM2(img_fruit1, 8)
    img_tamm = TAMM(img_fruit1)
    img_superres = SUPERRES(img_fruit1, img_fruit2) 

    # Salvar as novas imagens na pasta (convertendo de RGB de volta para BGR)
    cv2.imwrite('FRUIT1_aumentada_2x.jpg', cv2.cvtColor(img_tam2_2, cv2.COLOR_RGB2BGR))
    cv2.imwrite('FRUIT1_aumentada_8x.jpg', cv2.cvtColor(img_tam2_8, cv2.COLOR_RGB2BGR))
    cv2.imwrite('FRUIT1_TAMM.jpg', cv2.cvtColor(img_tamm, cv2.COLOR_RGB2BGR))
    cv2.imwrite('FRUIT_SUPERRES.jpg', cv2.cvtColor(img_superres, cv2.COLOR_RGB2BGR))
    
    print("As 4 imagens resultantes foram salvas na sua pasta.")

    # Mostrar as imagens no gráfico (Matplotlib)
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 4, 1)
    plt.imshow(img_tam2_2)
    plt.title('TAM2 (2x)')
    plt.axis('off')

    plt.subplot(1, 4, 2)
    plt.imshow(img_tam2_8)
    plt.title('TAM2 (8x)')
    plt.axis('off')

    plt.subplot(1, 4, 3)
    plt.imshow(img_tamm)
    plt.title('TAMM (2x)')
    plt.axis('off')

    plt.subplot(1, 4, 4)
    plt.imshow(img_superres)
    plt.title('SUPERRES')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

else:
    print("Erro: As imagens originais (FRUIT1.jpg ou FRUIT2.jpg) não foram encontradas.")