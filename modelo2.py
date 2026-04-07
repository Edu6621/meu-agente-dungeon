#Modelo 2

import random

class Agent:

    def __init__(self):
        self.posicao = (-1,-1) #inicializa memória 

    #Função booleana auxiliar para verificar se uma posição p está bloqueada.
    #Retorna True se p está fora do mapa ou se estiver ocupada por parede/bomba/agente 
    def tem_bloqueio(self, game_state, p):
        return not game_state.is_in_bounds(p) or game_state.entity_at(p) in ['sb','ib','ob','b',0,1]


    def next_move(self, game_state, player_state):
        ax, ay = player_state.location

        #Preenche a lista actions com ações possíveis ao redor do agente
        actions = [] 
        if (ax, ay+1) != self.posicao and not self.tem_bloqueio(game_state, (ax, ay+1)): #cima
            actions.append('u')
        if (ax, ay-1) != self.posicao and not self.tem_bloqueio(game_state, (ax, ay-1)): #baixo
            actions.append('d')
        if (ax+1, ay) != self.posicao and not self.tem_bloqueio(game_state, (ax+1, ay)): #direita
            actions.append('r')
        if (ax-1, ay) != self.posicao and not self.tem_bloqueio(game_state, (ax-1, ay)): #esquerda
            actions.append('l')

        self.posicao = (ax, ay) #Atualiza memória 

        if len(actions) > 0:
            return random.choice(actions) #Retorna um movimento aleatório entre os possíveis
        
        return '' #Fica parado nessa rodada se não pode se mover

