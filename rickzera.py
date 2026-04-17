#Agente baseado em Objetivo com Troca de Estados

#Estados implementados:

# - fugir: tenta se afastar da bomba 
# - coletar_tesouro: monta um plano para pegar um tesouro próximo 
# - coletar_municao: monta um plano para pegar uma municao proxima
# - atacar: joga uma bomba próxima se adjacente ao oponente 
# - seguir: tenta se aproximar do oponente 
# - explorar: faz um movimento aleatório simples

import random

from collections import deque

class Agent:

    def __init__(self):
        self.estado = "explorar"
    
    def tem_bloqueio(self, game_state, p):
        return not game_state.is_in_bounds(p) or game_state.entity_at(p) in ['sb','ib','ob','b',0,1]

    def distancia(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    #Retorna uma tupla (d,tx,ty) sendo a distancia do tesouro mais próximo e suas coordenadas.
    #Retorna 1000 na distância caso não existam tesouros.
    def tesouro_proximo(self, ax, ay, game_state):
        d = 1000  
        tx = -1
        ty = -1

        for tesouro_x, tesouro_y in game_state.treasure:
            dist = self.distancia((ax,ay),(tesouro_x, tesouro_y)) #distancia do tesouro até o agente
            if dist < d:
               d = dist
               tx = tesouro_x
               ty = tesouro_y

        return d, tx, ty

    def municao_proxima(self, ax, ay, game_state):
        d = 1000  
        mx = -1
        my = -1

        for municao_x, municao_y in game_state.ammo:
            dist = self.distancia((ax,ay),(municao_x, municao_y))
            if dist < d:
               d = dist
               mx = municao_x
               my = municao_y

        return d, mx, my

    def bomba_proxima(self, ax, ay, game_state):
        d = 1000 
        bx = -1
        by = -1

        for bomba_x, bomba_y in game_state.bombs:
            dist = self.distancia((ax,ay),(bomba_x, bomba_y)) 
            if dist < d:
               d = dist
               bx = bomba_x
               by = bomba_y

        return d, bx, by

    #Reconstrói uma rota até o ponto (mx,my) a partir de um dicionário
    #"visitados" que foi preenchido em um algoritmo de busca 
    def reconstroi(self, mx, my, visitados):
        rota = [(mx, my)]
        x,y = (mx, my)

        while visitados[(x,y)] is not None:
           x, y = visitados[(x,y)]
           if visitados[(x,y)] is not None:
               rota.append((x,y))

        return rota[::-1] #Inverte a lista

    #Retorna a ação que um agente no ponto a precisar realizar para se aproximar/afastar do ponto b
    #Recebe game_state
    #Recebe a: ponto (x,y) considerado como o agente que irá se mover
    #Recebe b: ponto (x,y) que é o ponto de referência
    #Recebe aproximar: se True o objetivo é se aproximar, caso contrário vai tentar afastar.
    #Retorna uma ação que mais aproxima ou afasta a de b. 
    def mover(self, game_state, a, b, aproximar=True):

        dist_ab = self.distancia(a,b) 

        actions = []
        adjacentes = {'u': (a[0],a[1]+1), 'r': (a[0]+1,a[1]), 'd': (a[0],a[1]-1), 'l':(a[0]-1,a[1])}
        for action, p in adjacentes.items():
           if not self.tem_bloqueio(game_state, p):
               dist_pb = self.distancia(p,b) 
               if (dist_pb > dist_ab and not aproximar) or (dist_pb < dist_ab and aproximar):
                   actions.append(action)

        if len(actions) > 0:
            return random.choice(actions)

        return ''

    #Retorna verdadeiro se o ponto (x,y) é uma posição livre no mapa.
    def posicao_livre(self, x, y, game_state, ocupados = ['sb','ob','ib','b']):
        b = game_state.is_in_bounds((x, y))
        e = game_state.entity_at((x,y)) 
        return (b and e not in ocupados)

    #Retorna uma lista com as posicões livres adjacentes a (ex,ey)     
    def vizinhanca_livre(self, ex, ey, game_state, ocupados = ['sb','ob','ib','b']):
        vizinhos = []
        #Coordenadas de   cima,      baixo,   esquerda,   direita
        posicoes = [(ex, ey-1), (ex, ey+1), (ex-1, ey), (ex+1, ey)]
        for px, py in posicoes:
            if self.posicao_livre(px, py, game_state, ocupados):
               vizinhos.append((px,py))
        return vizinhos
   
    #Calcula uma rota da origem (ox,oy) até uma meta (mx,my). 
    #A rota é uma lista de coordenadas ou uma lista vazia caso não exista uma rota
    #O motivo mais comum de uma rota não existir é a existência de obstaculos.
    #Como essa função usa a função vizinhanca_livre, a opção padrão do parâmetro 
    #`ocupados` determina o que será considerado um obstáculo.
    def busca_largura(self, ox, oy, mx, my, game_state, player_state):
        visitados = {}
        visitados[(ox, oy)] = None 
        fila = deque([(ox, oy)]) #criando a fila com a pos inicial
        
        while fila: #enquanto tiver elementos na fila
           ex, ey = fila.popleft() #retiramos elemento da esq. da fila
           if ex == mx and ey == my: #verifica se atingiu a meta
              return self.reconstroi(mx, my, visitados) 

           for x,y in self.vizinhanca_livre(ex, ey, game_state): 
              if (x,y) not in visitados:
                  visitados[(x,y)] = (ex, ey)
                  fila.append((x,y))
        return [] #Retorna uma rota vazia caso não encontre a meta
    
    #Função principal do jogo: deve retornar uma das ações abaixo:
    # 'u' = Andar para cima     
    # 'r' = Andar para direita  
    # 'd' = Andar para baixo    
    # 'l' = Andar para esquerda 
    # 'p' = Jogar bomba         
    # ''  = Ficar parado           
    def next_move(self, game_state, player_state):

        # SENSORES ========================================================
        ax, ay = player_state.location
        hx, hy = game_state.opponents(player_state.id)[0]
        distancia_humano = self.distancia((ax, ay), (hx, hy)) 
        distancia_bomba, bx, by = self.bomba_proxima(ax, ay, game_state)
        distancia_tesouro, tx, ty = self.tesouro_proximo(ax, ay, game_state)
        distancia_municao, mx, my = self.municao_proxima(ax, ay, game_state)


        # TRANSIÇÃO DE ESTADOS ============================================

        if distancia_bomba <=3:
            self.estado = "fugir"
        elif distancia_tesouro <= 3:
            self.estado = "coletar_tesouro"
        elif distancia_municao <= 3:
            self.estado = "coletar_municao"
        elif distancia_humano <=1:
            self.estado = "atacar"
        elif distancia_humano <= 3:
            self.estado = "seguir"
        else:
            self.estado = "explorar"

        print("Estado atual:", self.estado)


        # EXECUÇÃO DE AÇÕES ===============================================


        if self.estado == "fugir":
           return self.mover(game_state, (ax, ay), (bx, by), aproximar = False)

        if self.estado == "seguir":
           return self.mover(game_state, (ax, ay), (hx, hy), aproximar = True)

        if self.estado == "coletar_tesouro":
           rota = self.busca_largura(ax,ay,tx,ty, game_state, player_state) 
           if rota:
               return self.mover(game_state, (ax,ay), rota[0]) 

        if self.estado == "coletar_municao":
           rota = self.busca_largura(ax,ay,mx,my, game_state, player_state) 
           if rota:
               return self.mover(game_state, (ax,ay), rota[0]) 

        if self.estado == "atacar":
           return 'p'

        if self.estado == "explorar":
           return random.choice(['u','d','l','r'])

       
        return '' #Caso nenhuma ação seja possível fica parado por padrão.

