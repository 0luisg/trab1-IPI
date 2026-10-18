# Trabalho 1: Introdução ao Processamento de Imagens 🖼️

Este repositório contém a resolução do primeiro trabalho prático da disciplina de Introdução ao Processamento de Imagens. O projeto foca-se na manipulação direta de matrizes de imagem no domínio espacial através da linguagem Python, abordando técnicas de alteração de resolução espacial e de realce de contraste.

## 🚀 Funcionalidades e Algoritmos Implementados

O projeto está dividido em duas partes principais:

### Questão 1: Ampliação e Fusão Espacial (Sem redimensionamento nativo)
* **`TAM2` (Interpolação por Repetição):** Algoritmo iterativo que duplica a escala da imagem (testado em 2x e 8x) através da repetição direta de linhas e colunas (vizinho mais próximo).
* **`TAMM` (Expansão por Média):** Algoritmo de ampliação 2x que intercala os píxeis originais e preenche os espaços vazios calculando a média aritmética horizontal e vertical dos píxeis adjacentes, gerando bordas mais suaves.
* **`SUPERRES` (Super-resolução Híbrida):** Algoritmo que funde a informação de duas imagens distintas. A primeira imagem é mapeada nos índices pares da matriz e a segunda nos índices ímpares, sendo os "buracos" restantes preenchidos pela média espacial da vizinhança.

### Questão 2: Realce de Contraste e Radiometria
* **Correção Power-Law (Gama):** Implementação paramétrica ($s = c \cdot r^\gamma$) para recuperar fotografias subexpostas ($\gamma = 0.5$) ou sobre-expostas ($\gamma = 2.0$).
* **Equalização de Histograma:** Algoritmo de nivelamento da Função de Distribuição Acumulada (CDF). A equalização foi aplicada estritamente sobre o canal de luminância (Y) no espaço de cor YUV para evitar a distorção da matriz RGB original.
* **Geração de Gráficos:** Visualização analítica do Histograma e da curva CDF antes e após a equalização.

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **NumPy:** Para o manuseamento algébrico das matrizes multidimensionais.
* **OpenCV (`cv2`):** Para leitura, conversão de espaços de cor (BGR/RGB/YUV) e salvamento de ficheiros.
* **Matplotlib:** Para a renderização das grelhas de comparação visual e plotagem dos gráficos estatísticos (Histograma/CDF).

## ⚙️ Como Executar o Projeto localmente

**1. Clone este repositório:**
```
bash
git clone [https://github.com/0luisg/trab1-IPI.git](https://github.com/0luisg/trab1-IPI.git)
cd trab1-IPI

2. Instale as bibliotecas necessárias:
Bash
pip install opencv-python numpy matplotlib

3. Execute os scripts:
Certifique-se de que as imagens de teste (FRUIT1.jpg, FRUIT2.jpg, car.png, crowd.png, university.png) se encontram na mesma pasta dos arquivos Python.

Para a etapa de ampliação (Questão 1):
Bash
python teste.py

Para a etapa de realce e histogramas (Questão 2):
Bash
python questao2.py
