import cv2
import numpy as np
import heapq
#Tabelas
grafo = {}

#Inicializando imagem
img = cv2.imread('lolMapaMarcada.jpg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
_, binary_mask = cv2.threshold(blurred_img, 23, 255, cv2.THRESH_BINARY)
kernel = np.ones((3, 3), np.uint8)
binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel, iterations=2)

#Inicializando Grafo
altura, largura = binary_mask.shape

for y in range(altura):
    for x in range(largura):
        if binary_mask[y, x] > 0:
            grafo[(y, x)] = {}
            
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dy == 0 and dx == 0:
                        continue 

                    vizinho_y, vizinho_x = y + dy, x + dx

                    if 0 <= vizinho_y < altura and 0 <= vizinho_x < largura and binary_mask[vizinho_y, vizinho_x] > 0:
                        custo = 1.414 if dy != 0 and dx != 0 else 1
                        grafo[(y, x)][(vizinho_y, vizinho_x)] = custo

#Escolhendo início e fim
inicio_x = int(input("Inicio X:"))
inicio_y = int(input("Inicio y:"))

fim_x = int(input("Escolha o fim x: "))
fim_y = int(input("Escolha o fim y: "))

inicio = (inicio_y, inicio_x)
fim = (fim_y, fim_x)
if binary_mask[inicio] == 0:
    print("ERRO: O ponto de início está em um obstáculo!")
    exit()
if binary_mask[fim] == 0:
    print("ERRO: O ponto de fim está em um obstáculo!")
    exit()

#Tabela Custo
custos = {inicio: 0}
infinito = float("inf")

custos[inicio] = 0

#Tabela Pais
pais = {inicio: None}


#Algoritmo
processados = set() 


#Função do algoritmo
def menor_custo(custos):
    custo_mais_baixo = float("inf")
    nodo_custo_mais_baixo = None
    for nodo in custos:
        custo = custos[nodo]
        if custo < custo_mais_baixo and nodo not in processados:
            custo_mais_baixo = custo
            nodo_custo_mais_baixo = nodo
    return nodo_custo_mais_baixo


nodo = menor_custo(custos) 
fila_prioridade = [(0, inicio)]
while fila_prioridade:
    custo_atual, nodo_atual = heapq.heappop(fila_prioridade)
    if nodo_atual in processados:
        continue
    processados.add(nodo_atual)
    if nodo_atual == fim:
        break
    vizinhos = grafo.get(nodo_atual, {})
    for n_vizinho, peso in vizinhos.items():
        novo_custo = custo_atual + peso
        
        if n_vizinho not in custos or novo_custo < custos[n_vizinho]:
            custos[n_vizinho] = novo_custo
            pais[n_vizinho] = nodo_atual
            heapq.heappush(fila_prioridade, (novo_custo, n_vizinho))

if fim in pais:
    caminho_reverso = []
    nodo_atual = fim
    
    while nodo_atual is not None:
        caminho_reverso.append(nodo_atual)
        nodo_atual = pais.get(nodo_atual) 
        
    caminho_final = list(reversed(caminho_reverso))
    for passo in caminho_final:
        print(passo)



    for passo_yx in caminho_final:
        y, x = passo_yx
        img[y,x]=[0, 0, 255] 


print(nodo)
cv2.imshow('Máscara de Obstáculos', img)

cv2.waitKey(0)
cv2.destroyAllWindows()