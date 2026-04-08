# Exercício A : Seguir oponente por um tempo
# Modifique o agente para que ele funcione assim:
# se a distância até o oponente for maior ou igual a 5 o agente inicia uma perseguição.
# durante 50 iterações ele continua tentando se aproximar do oponente. Esse contador só pode ser atualizado
# novamente quando ele ficar parado.
# quando o contador termina, o agente deve ficar parado.

import random

class Agent:

    def __init__(self):
        self.contador = 0 #inicializa memória

    def tem_bloqueio(self, game_state, p):
        return not game_state.is_in_bounds(p) or game_state.entity_at(p) in ['sb','ib','ob','b',0,1]

    def next_move(self, game_state, player_state):

        #Pega coordenadas do agente, do oponente e do ponto na memória
        oponentes = game_state.opponents(player_state.id)
        ax, ay = player_state.location
        hx, hy = oponentes[0]

        #Calcula algumas distâncias
        dh = abs(ax - hx) + abs(ay - hy) #distancia até o oponente no ponto (hx,hy)
        
        #Se tiver perto do oponente
        if dh >= 5:
            self.contador = 50 #atualiza memória
            self.posicao = (ax, ay) #atualiza memória

        #Se o contador memorizado estiver positivo
        if self.contador > 0:
            self.contador = self.contador - 1 #atualiza memória

            #Guarda ações que aumentam a distancia até o ponto (px,py)
            actions = []
            if not self.tem_bloqueio(game_state, (ax, ay+1)): #cima
                d = abs(ax - hx) + abs((ay+1) - hy)
                if d < dh:
                    actions.append('u')

            if not self.tem_bloqueio(game_state, (ax, ay-1)): #baixo
                d = abs(ax - hx) + abs((ay-1) - hy)
                if d < dh:
                    actions.append('d')

            if not self.tem_bloqueio(game_state, (ax+1, ay)): #direita
                d = abs((ax+1) - hx) + abs(ay - hy)
                if d < dh:
                    actions.append('r')

            if not self.tem_bloqueio(game_state, (ax-1, ay)): #esquerda
                d = abs((ax-1) - hx) + abs(ay - hy)
                if d < dh:
                    actions.append('l')

            #Se tem alguma ação escolhe uma aleatoriamente
            if len(actions) > 0:
                return random.choice(actions)

        
        return ''

