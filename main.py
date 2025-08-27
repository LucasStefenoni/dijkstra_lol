import cv2
import numpy as np
import heapq
#Tabelas
grafo = {}

#Inicializando imagem
img = cv2.imread('lolMapa.png')

#Imagem para gerar grafos
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

                    if 0 <= vizinho_y < altura and 0 <= vizinho_x < largura and binary_mask[vizinho_y, vizinho_x] > 0: #Se o vizinho for válido
                        custo = 1.414 if dy != 0 and dx != 0 else 1 #1 se for vertical/horizontal, 1.414 (raiz de 2) se for diagonal
                        grafo[(y, x)][(vizinho_y, vizinho_x)] = custo

#Escolhendo início e fim
def escolher_pontos(nome):
    pontos = []
    nome_janela = nome
    img_copia = img.copy()

    def mouse_callback(event, x, y, flags, params): #Pegar clique no grafo do mapa
        if event == cv2.EVENT_LBUTTONDOWN and len(pontos) < 2:
            ponto_yx = (y, x)
            pontos.append(ponto_yx)
            if len(pontos) == 1:
                cv2.circle(img_copia, (x, y), 2, (0, 255, 0), -1) #Marcar início
            elif len(pontos) == 2:
                cv2.circle(img_copia, (x, y), 2, (0, 0, 255), -1) #Marcar fim

    cv2.namedWindow(nome_janela)
    cv2.setMouseCallback(nome_janela, mouse_callback)

    while len(pontos) < 2: #Esperar ter dois cliques (início e fim)
        cv2.imshow(nome_janela, img_copia)
        if cv2.waitKey(20) != -1: # Sair
            print("Seleção cancelada pelo usuário.")
            pontos = []
            cv2.destroyAllWindows()
            exit()

    cv2.imshow(nome_janela, img_copia)
    cv2.waitKey(500)
    cv2.destroyAllWindows()
    if pontos[0] not in grafo or pontos[1] not in grafo: #Verificar se os pontos são válidos
        print("Área inválida para início ou fim.")
        exit()
    return pontos


def calculando_caminho(cor,nome):
    inicio, fim = escolher_pontos(nome) 
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
            cv2.circle(img, (x, y), 1, (cor), -1)
        
    return custo_atual


#iniciando programa
def programa():
    global img
    aux_img = img.copy()
    custo_blue = calculando_caminho([255,0,0],"Aliado")
    custo_red = calculando_caminho([0,0,255],"Inimigo")
    cv2.imshow(f' B:{int (custo_blue)} | R:{int (custo_red)}', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    i = int(input("Deseja calcular outro caminho? 1[Sim] 0[Não]: "))
    img = aux_img.copy()
    if i == 1:
        programa()
    else:
        print("Encerrando...")
        exit()
programa()
cv2.destroyAllWindows()