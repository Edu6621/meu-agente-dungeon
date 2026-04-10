#Agente baseado em Objetivo com Troca de Estados

#Estados implementados:
# - explorar: faz um movimento aleatório em uma posição livre
# - seguir: segue o agente humano tentando encurtar a distância entre eles
# - atacar: joga uma bomba próxima ao agente humano
# - fugir: tenta ir para uma posição segura fora do raio da explosão
# - coletar_tesouro: tenta pegar um tesouro próximo 

import random

from collections import deque

class Agent:

    #Construtor da classe: serve para inicializar variáveis de estado interno
    def __init__(self):
        self.estado = "explorar" #Armazena o estado de ação do agente

    #Função booleana auxiliar para verificar se uma posição p está bloqueada.
    #Retorna True se p está fora do mapa ou se estiver ocupada por parede/bomba/agente 
    def tem_bloqueio(self, game_state, p):
        return not game_state.is_in_bounds(p) or game_state.entity_at(p) in ['sb','ib','ob','b',0,1]

    #Retorna a distância de Manhattan entre os pontos p1 e p2. 
    def distancia(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    #Retorna uma tupla (d,tx,ty) sendo a distancia do tesouro mais próximo e suas coordenadas.
    #Retorna 1000 na distância caso não existam tesouros.
    def tesouro_proximo(self, ax, ay, game_state):
        d = 1000 #começa com um valor "infinito" 
        tx = -1
        ty = -1

        for tesouro_x, tesouro_y in game_state.treasure:
            dist = self.distancia((ax,ay),(tesouro_x, tesouro_y)) #distancia do tesouro até o agente
            if dist < d:
               d = dist
               tx = tesouro_x
               ty = tesouro_y

        return d, tx, ty

    #Retorna uma tupla (d,tx,ty) sendo a distancia da bomba mais próxima e suas posição.
    #Retorna 1000 na distância caso não existam bombas.
    def bomba_proxima(self, ax, ay, game_state):
        d = 1000 #começa com um valor "infinito" 
        bx = -1
        by = -1

        for bomba_x, bomba_y in game_state.bombs:
            dist = self.distancia((ax,ay),(bomba_x, bomba_y)) #distancia da bomba até o agente
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

        #Se tem alguma ação escolhe uma aleatoriamente
        if len(actions) > 0:
            return random.choice(actions)

        #Senão retorna vazio
        return ''

    #Retorna verdadeiro se o ponto (x,y) é uma posição livre no mapa.
    #Para ser considerada livre a posição deve estar dentro dos limites
    #do mapa e não deve conter nenhum objeto indicado na lista "ocupados"
    #Por padrão, ocupados são apenas blocos de madeira, minério e indestrutível
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

        print("Estado:", self.estado)
        print("Tesouro", tx, ty, distancia_tesouro)
        print("Bomba", bx, by, distancia_bomba)

        # TRANSIÇÃO DE ESTADOS ============================================
        
        if distancia_bomba <= 3:
            self.estado = "fugir"
        elif distancia_tesouro <= 5:
            self.estado = "coletar_tesouro"
        elif distancia_humano <= 1:
            self.estado = "atacar"    
        else:
            self.estado = "explorar"    

        # EXECUÇÃO DE AÇÕES ===============================================

        if self.estado == "fugir":
            return self.mover(game_state, (ax, ay), (bx, by), aproximar = False)


        if self.estado == "coletar_tesouro":
            #Calcular rota
            rota = self.busca_largura(ax, ay, tx, ty, game_state, player_state)
            print(rota)
            if rota:
                return self.mover(game_state, (ax, ay), rota[0])

        if self.estado == "atacar":
           return 'p'

        if self.estado == "explorar":
           return random.choice(['u','d','l','r'])

        if distancia_tesouro <=5:
            self.estado = "coletar_tesouro"

       
        return '' #Caso nenhuma ação seja possível fica parado por padrão.

