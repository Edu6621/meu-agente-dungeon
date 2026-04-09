#Modelo C

import random

class Agent:

    def __init__(self):
        self.contador = 0 #inicializa memória
        self.rota = [] #rota usada para fuga
        self.alvo = (-1,-1) #posicao do alvo

    #Função booleana auxiliar para verificar se uma posição p está bloqueada.
    #Retorna True se p está fora do mapa ou se estiver ocupada por parede/bomba/agente 
    def tem_bloqueio(self, game_state, p):
        return not game_state.is_in_bounds(p) or game_state.entity_at(p) in ['sb','ib','ob','b',0,1]


    #Função que calcula a distância de Manhattan entre p1 e p2
    #Recebe p1 como uma tupla (x,y)
    #Recebe p2 como uma tupla (x,y)
    #Retorna um número
    def distancia(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) 


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
        

    def next_move(self, game_state, player_state):

        #Pega coordenadas do agente e municao
        ax, ay = player_state.location
        municao = player_state.ammo
        
        if self.contador == 0 and municao > 0:
            #Cria uma lista com posições possíveis onde pode haver um bomba
            posicoes = [(ax,ay),(ax,ay+1), (ax+1,ay), (ax,ay-1), (ax-1,ay)]
           
            #Verifica se uma das posições da lista é bloco de minério (ob)
            for p in posicoes:
                if game_state.entity_at(p) == 'ob':
                    self.contador = 40 #atualiza memória
                    return 'p' #joga bomba

        #Se o contador memorizado estiver positivo até a metade 
        if self.contador > 20:
            print("Afastando",self.contador)
            self.contador = self.contador - 1 #atualiza memória
            action = self.mover(game_state, (ax, ay), self.alvo, aproximar=False) 
            self.rota.append((ax,ay)) #atualiza memória da rota de volta
            return action

        #Se o contador memorizado estiver positivo
        if self.contador > 0:
            print("Voltando",self.contador)
            self.contador = self.contador - 1 #atualiza memória
            p = self.rota.pop() #retira da lista última posição da rota
            action = self.mover(game_state, (ax, ay), p, aproximar=True) 
            return action

        return random.choice(['u','d','l','r']) #Aleatório por padrão
