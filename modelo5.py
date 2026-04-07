#Modelo 5

import random

class Agent:

    def __init__(self):
        self.contador = 0 #inicializa memória
        self.posicao = (-1,-1) #inicializa memória

    #Função booleana auxiliar para verificar se uma posição p está bloqueada.
    #Retorna True se p está fora do mapa ou se estiver ocupada por parede/bomba/agente 
    def tem_bloqueio(self, game_state, p):
        return not game_state.is_in_bounds(p) or game_state.entity_at(p) in ['sb','ib','ob','b',0,1]

    def next_move(self, game_state, player_state):

        #Pega coordenadas do agente, do oponente e do ponto na memória
        oponentes = game_state.opponents(player_state.id)
        ax, ay = player_state.location
        hx, hy = oponentes[0]
        px, py = self.posicao

        #Calcula algumas distâncias
        dh = abs(ax - hx) + abs(ay - hy) #distancia até o oponente no ponto (hx,hy)
        dp = abs(ax - px) + abs(ay - py) #distancia até o ponto em memória (px,py)

        #Se tiver perto do oponente
        if dh <= 2:
            self.contador = 7 #atualiza memória
            self.posicao = (ax, ay) #atualiza memória

        #Se o contador memorizado estiver positivo
        if self.contador > 0:
            self.contador = self.contador - 1 #atualiza memória

            #Guarda ações que aumentam a distancia até o ponto (px,py)
            actions = []
            if not self.tem_bloqueio(game_state, (ax, ay+1)): #cima
                d = abs(ax - px) + abs((ay+1) - py)
                if d > dp:
                    actions.append('u')

            if not self.tem_bloqueio(game_state, (ax, ay-1)): #baixo
                d = abs(ax - px) + abs((ay-1) - py)
                if d > dp:
                    actions.append('d')

            if not self.tem_bloqueio(game_state, (ax+1, ay)): #direita
                d = abs((ax+1) - px) + abs(ay - py)
                if d > dp:
                    actions.append('r')

            if not self.tem_bloqueio(game_state, (ax-1, ay)): #esquerda
                d = abs((ax-1) - px) + abs(ay - py)
                if d > dp:
                    actions.append('l')

            #Se tem alguma ação escolhe uma aleatoriamente
            if len(actions) > 0:
                return random.choice(actions)

        return '' #Fica parado por padrão
