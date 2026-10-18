import cv2
import numpy as np
import matplotlib.pyplot as plt
import os  # <--- NOVA BIBLIOTECA ADICIONADA AQUI

# ==========================================
# 1. DEFINIÇÃO DAS FUNÇÕES
# ==========================================

def power_law(img, gamma):
    img_normalizada = img / 255.0
    res = np.power(img_normalizada, gamma)
    return np.uint8(res * 255)

def equalizar_imagem_rgb(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)

def calcular_e_mostrar_histograma_cdf(img, titulo):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    hist, _ = np.histogram(img_gray.flatten(), 256, range=[0,256])
    
    cdf = hist.cumsum()
    if cdf.max() > 0:
        cdf_normalizada = cdf * float(hist.max()) / cdf.max()
    else:
        cdf_normalizada = cdf

    plt.figure(figsize=(8, 4))
    plt.plot(cdf_normalizada, color='b', label='CDF')
    plt.hist(img_gray.flatten(), 256, range=[0,256], color='r', label='Histograma')
    plt.xlim([0, 256])
    plt.legend(loc='upper left')
    plt.title(titulo)
    plt.show()

# ==========================================
# 2. TESTES, CRIAÇÃO DE PASTAS E GUARDA
# ==========================================

nomes_imagens = ['car.png', 'crowd.png', 'university.png']

for nome in nomes_imagens:
    # Carregar imagem
    img = cv2.imread(nome)
    if img is None:
        print(f"Erro: Não foi possível carregar {nome}. Verifique se está na pasta.")
        continue
        
    # Converter para RGB para o processamento
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Executar os processamentos
    img_gamma_05 = power_law(img_rgb, 0.5) 
    img_gamma_20 = power_law(img_rgb, 2.0) 
    img_eq = equalizar_imagem_rgb(img_rgb)
    
    # -----------------------------------------------------
    # NOVA LÓGICA: CRIAR PASTA E SALVAR AS 4 IMAGENS
    # -----------------------------------------------------
    # Pega apenas o nome sem a extensão (ex: 'car' de 'car.png')
    nome_pasta = nome.split('.')[0]
    
    # Cria a pasta se ela não existir
    os.makedirs(nome_pasta, exist_ok=True)
    
    # Converter tudo de volta para BGR antes de guardar
    bgr_original = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    bgr_gamma_05 = cv2.cvtColor(img_gamma_05, cv2.COLOR_RGB2BGR)
    bgr_gamma_20 = cv2.cvtColor(img_gamma_20, cv2.COLOR_RGB2BGR)
    bgr_eq = cv2.cvtColor(img_eq, cv2.COLOR_RGB2BGR)
    
    # Definir caminhos e guardar (ex: car/original_car.png)
    cv2.imwrite(os.path.join(nome_pasta, f"1_original_{nome}"), bgr_original)
    cv2.imwrite(os.path.join(nome_pasta, f"2_powerlaw_0.5_{nome}"), bgr_gamma_05)
    cv2.imwrite(os.path.join(nome_pasta, f"3_powerlaw_2.0_{nome}"), bgr_gamma_20)
    cv2.imwrite(os.path.join(nome_pasta, f"4_equalizada_{nome}"), bgr_eq)
    
    print(f"✔️ As 4 imagens foram guardadas na pasta: '{nome_pasta}'")
    # -----------------------------------------------------
    
    # (Opcional) Mostrar os resultados na tela (Gráficos Matplotlib)
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 4, 1)
    plt.imshow(img_rgb)
    plt.title(f'Original: {nome}')
    plt.axis('off')
    
    plt.subplot(1, 4, 2)
    plt.imshow(img_gamma_05)
    plt.title('Power-Law (Gamma=0.5)')
    plt.axis('off')
    
    plt.subplot(1, 4, 3)
    plt.imshow(img_gamma_20)
    plt.title('Power-Law (Gamma=2.0)')
    plt.axis('off')
    
    plt.subplot(1, 4, 4)
    plt.imshow(img_eq)
    plt.title('Equalizada')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

    # Mostrar histograma apenas do carro
    if nome == 'car.png':
        calcular_e_mostrar_histograma_cdf(img_rgb, f"Antes da Equalização - {nome}")
        calcular_e_mostrar_histograma_cdf(img_eq, f"Depois da Equalização - {nome}")