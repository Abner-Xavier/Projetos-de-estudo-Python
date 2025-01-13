import pygame
from heapq import heappop, heappush

# Inicialização do Pygame
pygame.init()

# Dimensões da tela e do mapa
LARGURA, ALTURA = 840, 600
TAMANHO_BLOCO = 40

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)

# Configuração da tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pac-Man com A*")

# Relógio para FPS
relogio = pygame.time.Clock()

# Mapa do jogo (1 = parede, 0 = caminho)
MAPA = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Posição inicial do jogador
posicao_jogador = [10, 7]

# Posição inicial do inimigo
posicao_inimigo = [7, 11]

# Posição intermediária do inimigo para movimento suave
posicao_inimigo_intermediaria = [posicao_inimigo[0] * TAMANHO_BLOCO, posicao_inimigo[1] * TAMANHO_BLOCO]

# Velocidade do inimigo (pixels por frame)
velocidade_inimigo = 2

# Lista de pontos no mapa
pontos = [(5, 3), (5, 2), (5, 7), (7, 5), (11, 11)]

# Adicionar pontos de forma simplificada
pontos.extend([(1, coluna) for coluna in range(1, 20)])
pontos.extend([(13, coluna) for coluna in range(1, 20)])
pontos.extend([(7, coluna) for coluna in range(1, 20)])
pontos.extend([(3, coluna) for coluna in range(3, 18)])
pontos.extend([(11, coluna) for coluna in range(3, 18)])
pontos.extend([(1, linha) for linha in range(2, 6)])
pontos.extend([(linha, 1) for linha in range(1, 14)])
pontos.extend([(linha, 3) for linha in range(3, 5)])
pontos.extend([(linha, 19) for linha in range(1, 14)])



# Função para desenhar o mapa
def desenhar_mapa():
    for linha_index, linha in enumerate(MAPA):
        for coluna_index, bloco in enumerate(linha):
            x = coluna_index * TAMANHO_BLOCO
            y = linha_index * TAMANHO_BLOCO
            cor = AZUL if bloco == 1 else PRETO
            pygame.draw.rect(tela, cor, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))

# Função para desenhar o jogador
def desenhar_jogador():
    x = posicao_jogador[1] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
    y = posicao_jogador[0] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
    pygame.draw.circle(tela, AMARELO, (x, y), TAMANHO_BLOCO // 3)

# Função para desenhar os pontos
def desenhar_pontos():
    for ponto in pontos:
        x = ponto[1] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
        y = ponto[0] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
        pygame.draw.circle(tela, BRANCO, (x, y), TAMANHO_BLOCO // 5)

# Função para coletar pontos pelo jogador
def coletar_pontos():
    global pontos
    jogador_pos = (posicao_jogador[0], posicao_jogador[1])
    if jogador_pos in pontos:
        pontos.remove(jogador_pos)

# Função para desenhar o inimigo
def desenhar_inimigo():
    x = posicao_inimigo_intermediaria[1]
    y = posicao_inimigo_intermediaria[0]
    pygame.draw.circle(tela, VERMELHO, (x, y), TAMANHO_BLOCO // 3)

# Movimentação do jogador
def mover_jogador(dx, dy):
    nova_linha = posicao_jogador[0] + dy
    nova_coluna = posicao_jogador[1] + dx
    if MAPA[nova_linha][nova_coluna] == 0:  # Verifica se não é parede
        posicao_jogador[0] = nova_linha
        posicao_jogador[1] = nova_coluna

# Função heurística para A* (distância de Manhattan)
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Algoritmo A* para encontrar o menor caminho
def a_estrela(inicio, objetivo):
    aberto = []
    heappush(aberto, (0, inicio))
    veio_de = {}
    custo_g = {inicio: 0}
    custo_f = {inicio: heuristica(inicio, objetivo)}

    while aberto:
        _, atual = heappop(aberto)

        if atual == objetivo:
            caminho = []
            while atual in veio_de:
                caminho.append(atual)
                atual = veio_de[atual]
            return caminho[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            vizinho = (atual[0] + dx, atual[1] + dy)
            if MAPA[vizinho[0]][vizinho[1]] == 1:
                continue
            custo_temporario_g = custo_g[atual] + 1
            if custo_temporario_g < custo_g.get(vizinho, float('inf')):
                veio_de[vizinho] = atual
                custo_g[vizinho] = custo_temporario_g
                custo_f[vizinho] = custo_temporario_g + heuristica(vizinho, objetivo)
                heappush(aberto, (custo_f[vizinho], vizinho))

    return []

# Movimentação do inimigo
def mover_inimigo():
    global posicao_inimigo_intermediaria, posicao_inimigo

    destino_x = posicao_inimigo[1] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
    destino_y = posicao_inimigo[0] * TAMANHO_BLOCO + TAMANHO_BLOCO // 2

    if posicao_inimigo_intermediaria[0] < destino_y:
        posicao_inimigo_intermediaria[0] += velocidade_inimigo
    elif posicao_inimigo_intermediaria[0] > destino_y:
        posicao_inimigo_intermediaria[0] -= velocidade_inimigo

    if posicao_inimigo_intermediaria[1] < destino_x:
        posicao_inimigo_intermediaria[1] += velocidade_inimigo
    elif posicao_inimigo_intermediaria[1] > destino_x:
        posicao_inimigo_intermediaria[1] -= velocidade_inimigo

    if (posicao_inimigo_intermediaria[0] == destino_y and
        posicao_inimigo_intermediaria[1] == destino_x):
        caminho = a_estrela(tuple(posicao_inimigo), tuple(posicao_jogador))
        if caminho:
            posicao_inimigo[0], posicao_inimigo[1] = caminho[0]

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                mover_jogador(0, -1)
            elif evento.key == pygame.K_DOWN:
                mover_jogador(0, 1)
            elif evento.key == pygame.K_LEFT:
                mover_jogador(-1, 0)
            elif evento.key == pygame.K_RIGHT:
                mover_jogador(1, 0)

    coletar_pontos()

    tela.fill(PRETO)
    desenhar_mapa()
    desenhar_pontos()
    desenhar_jogador()
    mover_inimigo()
    desenhar_inimigo()
    pygame.display.flip()
    relogio.tick(50)


pygame.quit()